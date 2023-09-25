from djoser.serializers import UserCreateSerializer

from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for Users."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
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


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for Subscriptions."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
        )
