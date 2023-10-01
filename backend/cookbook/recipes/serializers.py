import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

from rest_framework import serializers

#from users.serializers import UserSerializer

from .models import (
    Ingredient,
    Ingredient_Recipe,
    Recipe,
    Recipe_Tag,
    Tag,
)


class RecipeInfoSerializer(serializers.ModelSerializer):
    """Serializer for common information about Recipe."""
    class Meta:
        model = Recipe
        fields = (
            'name', 
            'about',
            'author',
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


class IngredientInRecipeSerializer(serializers.Serializer):
    """Serializer for ingredients in the Recipe."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        min_value=0.001
    )


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe model."""
    image = Base64ImageField()
    #author = UserSerializer(
    #    read_only=True
    #)
    ingredients = IngredientInRecipeSerializer(
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True, 
    )

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = (
            'author',
            'ingredients',
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        for item in ingredients:
            ingredient = get_object_or_404(
                Ingredient,
                id=item.get('id'),
            )
            Ingredient_Recipe.objects.create(
                ingredient=ingredient,
                recipe=recipe,
                amount=item.get('amount'),
            )

        for item in tags:
            Recipe_Tag.objects.create(
                tag=item,
                recipe=recipe,
            )

        return recipe
