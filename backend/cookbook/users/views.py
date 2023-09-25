from django.contrib.auth import get_user_model
from djoser.views import UserViewSet

from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import SubscriptionSerializer


class UserViewSet(UserViewSet):
    """Кастомизированный вьюсет библиотеки 'djoser'."""
    @action(
        methods=['get'],
        detail=False,
        serializer_class=SubscriptionSerializer
    )
    def subscriptions(self, request):
        pass

    @action(
        methods=['post', 'delete'], 
        detail=True,
        serializer_class=SubscriptionSerializer
    )
    def subscribe(self, request, id):
        pass
