from djoser.serializers import UserCreateSerializer

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import (
    Follow,
    User
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
        user = self.context['request'].user
        return (
            user.is_authenticated and
            data.follower.filter(
                following = user
            ).exists()
        )


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

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
        )


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
        if data['user'] == data['author']:
            raise serializers.ValidationError(
                'Self suscription is not allowed.'
            )
        return data
