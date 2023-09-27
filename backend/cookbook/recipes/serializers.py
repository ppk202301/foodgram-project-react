from rest_framework import serializers

from .models import (
    Tag,
    Recipe,
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

