from rest_framework import serializers

from .models import (
    Recipe
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
