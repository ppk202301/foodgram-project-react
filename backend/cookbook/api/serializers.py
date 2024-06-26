import base64

from django.contrib.auth.models import AnonymousUser
from django.core.files.base import ContentFile

from rest_framework import serializers

from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueTogetherValidator

from .serializers_users import (
    UserSerializer
)

from recipes.models import (
    Cart,
    Favorite,
    Ingredient,
    IngredientRecipe,
    MIN_AMOUNT,
    MIN_COOKING_TIME,
    Recipe,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    """Serilizer for Tag model."""
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Serilizer for Ingredient model."""
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Serializer for ingredients in the Recipe."""
    id = serializers.ReadOnlyField(
        source='ingredient.id',
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name',
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class Base64ImageField(serializers.ImageField):
    """Serializer for image decording."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imgstr),
                name='temp.' + ext,
            )

        return super().to_internal_value(data)


class IngredientRecipeSaveSerializer(serializers.Serializer):
    """Serializer for ingredients of the recipe."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        min_value=MIN_AMOUNT,
    )


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe model."""
    tags = TagSerializer(
        many=True
    )
    author = UserSerializer(
        default=CurrentUserDefault()
    )
    ingredients = IngredientInRecipeSerializer(
        many=True,
        read_only=True,
        source='recipes',
    )
    is_favorited = serializers.SerializerMethodField(
        read_only=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        exclude = ('pub_date',)

    def get_is_favorited(self, obj):
        user = self.context['request'].user

        if isinstance(user, AnonymousUser):
            return False

        return Favorite.objects.filter(
            recipe=obj,
            user=self.context['request'].user,
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if isinstance(user, AnonymousUser):
            return False

        return Cart.objects.filter(
            recipe=obj,
            user=self.context['request'].user,
        ).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Serializer for new recipe creation."""
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    author = UserSerializer(
        default=CurrentUserDefault()
    )
    ingredients = IngredientRecipeSaveSerializer(
        many=True,
        source='IngredientRecipe',
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        exclude = ('pub_date',)
        read_only_fields = (
            'author',
        )

    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        )
        return serializer.data

    def validate_ingredients(self, data):
        """Ingredients list validation."""
        if data is None:
            raise serializers.ValidationError(
                'No ingredient is found.'
            )
        if len(data) < 1:
            raise serializers.ValidationError(
                'Number of ingredients is too small.'
            )

        ingredients_list = []
        for el in data:
            if not Ingredient.objects.filter(pk=el['id']).exists():
                raise serializers.ValidationError(
                    f'Ingredient {el} is not found in the database')
            ingredients_list.append(el['id'])

        if len(ingredients_list) != len(set(ingredients_list)):
            raise serializers.ValidationError(
                'Ingredients should be unique in the request.')
        return data

    def validate_cooking_time(self, data):
        """Cooking time validation."""
        if data is None:
            raise serializers.ValidationError(
                'No production time value is found.'
            )
        if not (str(data).isdigit()):
            raise serializers.ValidationError(
                f'Production time shoud be a number. Found: {data}'
            )
        if int(data) < MIN_COOKING_TIME:
            raise serializers.ValidationError(
                f'Production time should be more than '
                f'{MIN_COOKING_TIME} min. Found: {data}'
            )
        return data

    def validate_text(self, data):
        """Recipe description validation."""
        if data is None:
            raise serializers.ValidationError(
                'No description (text) is found.'
            )

        if str(data) == '':
            raise serializers.ValidationError(
                'The description could not be empty.'
            )
        return data

    def validate_tags(self, data):
        """Tags list validation."""
        if data is None:
            raise serializers.ValidationError(
                'No tag is found.'
            )

        if len(data) < 1:
            raise serializers.ValidationError(
                'Number of tags is too small.'
            )
        if len(data) != len(set(data)):
            raise serializers.ValidationError(
                'Tags should be unique in the request.'
            )
        return data

    def _add_ingredients_list(self, recipe, ingredients):
        """Add list of ingredients."""
        data = []

        for ingredient in ingredients:
            data.append(
                IngredientRecipe(
                    recipe=recipe,
                    amount=ingredient['amount'],
                    ingredient_id=ingredient['id'],
                )
            )

        IngredientRecipe.objects.bulk_create(data)

    def create(self, validated_data):
        """Create new recipe."""
        tags = validated_data.pop(
            'tags'
        )
        ingredients = validated_data.pop(
            'IngredientRecipe'
        )
        recipe = Recipe.objects.create(
            **validated_data
        )

        recipe.tags.set(tags)

        self._add_ingredients_list(
            recipe,
            ingredients
        )

        return recipe


class RecipeUpdateSerializer(RecipeCreateSerializer):
    """Serializer for recipe update."""
    def update(self, instance, validated_data):
        """Update the recipe."""
        if 'tags' in validated_data:
            instance.tags.set(
                validated_data.pop('tags')
            )
        if 'IngredientRecipe' in validated_data:
            ingredients = validated_data.pop(
                'IngredientRecipe'
            )
        else:
            raise serializers.ValidationError(
                'Update of the recipe. Correct ingredient list is not found.'
            )

        instance.name = validated_data.get(
            'name',
            instance.name
        )
        instance.image = validated_data.get(
            'image',
            instance.image
        )
        instance.text = validated_data.get(
            'text',
            instance.text
        )
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )

        if ingredients is not None:
            instance.ingredients.clear()
        instance.save()

        self._add_ingredients_list(
            instance,
            ingredients
        )
        return instance

    def validate(self, attrs):
        """Data validation."""
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')

        ingredients_list = []

        if ingredients:
            for ingredient in ingredients:
                ingredients_list.append(
                    ingredient.get('id')
                )
            if len(ingredients_list) != len(set(ingredients_list)):
                raise serializers.ValidationError(
                    'Ingredients should be unique in the request.')

        if tags:
            if len(tags) != len(set(tags)):
                raise serializers.ValidationError(
                    'Tags should be unique in the request.'
                )

        return attrs


class RecipeMainInfoSerializer(serializers.ModelSerializer):
    """Serializer for main information about the recipe."""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        read_only_fields = (
            'name',
            'image',
            'cooking_time',
        )


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for Favorite model."""
    class Meta:
        model = Favorite
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                message='This recipe is in user\'s. favorite list already.',
                fields=(
                    'recipe',
                    'user',
                ),
            )
        ]


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart model."""
    class Meta:
        model = Cart
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Cart.objects.all(),
                message='This recipe is in user\'s. cart list already.',
                fields=(
                    'recipe',
                    'user',
                ),
            )
        ]
