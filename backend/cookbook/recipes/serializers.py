import base64

from django.contrib.auth.models import  AnonymousUser
from django.core.files.base import ContentFile

from rest_framework import serializers

from rest_framework.fields import CurrentUserDefault

from users.models import User
from users.serializers import (
    UserSerializer
)

from .models import (
    Cart,
    Favorite,
    Ingredient,
    Ingredient_Recipe,
    MIN_AMOUNT,
    Recipe,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    """Serilizer for Tag model."""
    
    print(f'Debugging: work TagSerializer')

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


class IngredientInRecipeSerializer(serializers.Serializer):
    """Serializer for ingredients in the Recipe."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        min_value=0.001
    )


class Base64ImageField(serializers.ImageField):
    """Serializer for image decording."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imgstr),
                name='temp.' + ext
            )

        return super().to_internal_value(data)


class Ingredient_RecipeSaveSerializer(serializers.Serializer):
    """Serializer for ingredients of the recipe."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        min_value=MIN_AMOUNT,
    )


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe model."""

    print(f'Debugging: work RecipeSerializer')

    tags = TagSerializer(
        many=True
    )
    author = UserSerializer(
        default=CurrentUserDefault()
    )
    ingredients = IngredientSerializer(
        many=True,
        read_only=True,
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

        print(f'Debugging: work get_is_favorited')
        print(f'Debugging: work get_is_favorited self = {self}')
        print(f'Debugging: work get_is_favorited obj = {obj}')

        user=self.context['request'].user
        print(f'Debugging: work get_is_favorited user = {user}')

        if isinstance(user, AnonymousUser):
            return False

        return Favorite.objects.filter(
            recipe=obj,
            user=self.context['request'].user,
        ).exists()

    def get_is_in_shopping_cart(self, obj):

        print(f'Debugging: work get_is_in_shopping_cart')
        #print(f'Debugging: work get_is_in_shopping_cart self = {self}')
        user=self.context['request'].user
        print(f'Debugging: work get_is_in_shopping_cart user = {user}')

        if isinstance(user, AnonymousUser):
            return False

        return Cart.objects.filter(
            recipe=obj,
            user=self.context['request'].user,
        ).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Serializer for new recipe creation."""

    print(f'Debugging: work RecipeCreateSerializer')

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )

    print(f'Debugging: tags = {tags}')

    author = UserSerializer(
        default=CurrentUserDefault()
    )

    print(f'Debugging: author = {author}')

    ingredients = Ingredient_RecipeSaveSerializer(
        many=True,
        source='Ingredient_Recipe',
    )

    print(f'Debugging: ingredients = {ingredients}')

    image = Base64ImageField()

    class Meta:
        model = Recipe
        exclude = ('pub_date',)
        read_only_fields = (
            'author',
        )

    def to_representation(self, instance):

        print(f'Debugging: work to_representation')
        print(f'Debugging: work to_representation self = {self}')
        print(f'Debugging: work to_representation instance = {instance}')

        #print(f'Debugging: work to_representation instance keys = {instance.keys()}')

        #tags = instance.get('tags')

        #print(f'Debugging: work to_representation instance key tags = {tags}')

        #print(f'Debugging: work to_representation instance key tags [0]= {tags[0]}')

        #print(f'Debugging: work to_representation instance key tags [0] name= {tags[0].name}')
        #print(f'Debugging: work to_representation instance key tags [0] color= {tags[0].color}')
        #print(f'Debugging: work to_representation instance key tags [0] slug = {tags[0].slug}')

        serializer = RecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        )

        print(f'Debugging: work to_representation serializer = {serializer}')
        print(f'Debugging: work to_representation serializer.data = {serializer.data}')

        return serializer.data

    def validate(self, attrs):
        """Data validation."""

        print(f'Debugging: work validate')
        print(f'Debugging: validate self = {self}')
        print(f'Debugging: validate begining attr = {attrs}')

        ingredients = self.initial_data.get(
            'ingredients'
        )
        if not ingredients:
            raise serializers.ValidationError(
                'No engidient is found.'
            )
        ingredients_list = []
        for ingredient in ingredients:
            ingredients_list.append(
                ingredient.get('id')
            )
        if len(ingredients_list) != len(set(ingredients_list)):
            raise serializers.ValidationError(
                'Ingredients should be unique in the request.')

        tags = self.initial_data.get(
            'tags'
        )
        if not tags:
            raise serializers.ValidationError(
                'No tag is found.'
            )
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError(
                'Tags should be unique in the request.'
            )
    
        text = self.initial_data.get(
            'text'
        )
        if not text:
            raise serializers.ValidationError(
                'No description (text) is found.'
            )
        if str(text) == '':
            raise serializers.ValidationError(
                'The description could not be empty.'
            )

        cooking_time = self.initial_data.get(
            'cooking_time'
        )
        if not cooking_time:
            raise serializers.ValidationError(
                'No cooking_time value is found.'
            )

        print(f'Debugging: validate end attr = {attrs}')

        return attrs

    def _add_ingredients_list(self, recipe, ingredients):
        """Add list of ingredients."""

        print(f'Debugging: _add_ingredients_list')
        print(f'Debugging: _add_ingredients_list self = {self}')
        print(f'Debugging: _add_ingredients_list recipe = {recipe}')
        print(f'Debugging: _add_ingredients_list ingredients = {ingredients}')

        if ingredients is None:
            print(f'Debugging: _add_ingredients_list Ingredients are not found')
            return

        data = []

        for ingredient in ingredients:
            print(f'Debugging: _add_ingredients_list ingredient = {ingredient}')
            data.append(
                Ingredient_Recipe(
                    recipe=recipe,
                    amount=ingredient['amount'],
                    ingredient_id=ingredient['id'],
                )
            )

        print(f'Debugging: _add_ingredients_list data = {data}')

        Ingredient_Recipe.objects.bulk_create(data)

    def create(self, validated_data):
        """Create new recipe."""

        print(f'Debugging: work serializer create')
        print(f'Debugging: validated_data = {validated_data}')

        tags = validated_data.pop(
            'tags'
        )

        print(f'Debugging: tags = {tags}')

        ingredients = validated_data.pop(
            'Ingredient_Recipe'
        )

        print(f'Debugging: ingredients = {ingredients}')

        print(f'Debugging serializer create: validated_data = {validated_data}')

        recipe = Recipe.objects.create(
            **validated_data
        )

        print(f'Debugging: recipe before tags = {recipe}')

        for tag in tags:
            recipe.tags.add(tag)

        print(f'Debugging: recipe after tags = {recipe}')

        self._add_ingredients_list(
            recipe,
            ingredients
        )

        print(f'Debugging: recipe after _add_ingredients_list = {recipe}')

        return recipe

 
class RecipeUpdateSerializer(RecipeCreateSerializer):
    """Serializer for recipe update."""
    def update(self, instance, validated_data):
        """Update the recipe."""

        print(f'Debugging: work RecipeUpdateSerializer')

        print(f'Debugging: work RecipeUpdateSerializer self = {self}')
        print(f'Debugging: work RecipeUpdateSerializer instance = {instance}')
        print(f'Debugging: work RecipeUpdateSerializer validated_date = {validated_data}')

        if 'tags' in validated_data:
            instance.tags.set(
                validated_data.pop('tags')
            )

        if 'Ingredient_Recipe' in validated_data:
            ingredients = validated_data.pop(
                'Ingredient_Recipe'
            )
        else:
            ingredients = None

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

        print(f'Debugging: work validate')
        print(f'Debugging: validate self = {self}')
        print(f'Debugging: validate begining attr = {attrs}')

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

        print(f'Debugging: validate end attr = {attrs}')

        return attrs