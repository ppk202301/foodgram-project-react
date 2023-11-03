from djoser.serializers import UserCreateSerializer

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Recipe

from users.models import (
    Follow,
    User
)

from users.utils import (
    is_subscribed
)


class RecipeInfoSerializer(serializers.ModelSerializer):
    """Serializer for common information about Recipe."""
    class Meta:
        model = Recipe
        fields = (
            'name',
            'text',
            'author',
        )


class UserSerializer(serializers.ModelSerializer):
    """Serializer for Users."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_subscribed',
        )

    def get_is_subscribed(self, data):
        return is_subscribed(self, data)


class UserCreationSerializer(UserCreateSerializer):
    """Serializer for Users creation."""
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for Follow."""
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_subscribed',
            'recipes_count',
            'recipes',
        )

    def get_recipes_count(self, data):
        return data.recipes.count()

    def get_is_subscribed(self, data):
        return is_subscribed(self, data)

    def get_recipes(self, data):
        recipes_limit = self.context.get(
            'request'
        ).GET.get(
            'recipes_limit'
        )
        recipes = data.recipes.all()

        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]

        serializer = RecipeInfoSerializer(
            recipes,
            read_only=True,
            many=True,
        )

        return serializer.data


class FollowSaveNewSerializer(FollowSerializer):
    """Serializer for saving new follower."""
    def get_is_subscribed(self, data):
        return True


class FollowCreateSerializer(serializers.ModelSerializer):
    """Serializer for Follow creation."""
    class Meta:
        model = Follow
        fields = (
            'user',
            'following',
        )

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=(
                    'following',
                    'user',
                ),
                message='There is your subscription to this user.'
            )
        ]

    def validate(self, data):
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                'Self suscription is not allowed.'
            )

        return data
