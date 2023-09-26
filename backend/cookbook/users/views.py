from django.contrib.auth import get_user_model
from djoser.views import UserViewSet

from rest_framework import (
    serializers,
    status
)
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import (
    FollowCreateSerializer,
    FollowSerializer,
)

class UserViewSet(UserViewSet):
    """User Viewset"""
    @action(
        methods=['post', 'delete'], 
        serializer_class=FollowSerializer,
        detail=True,
    )
    def subscribe(self, request, id):
        user = self.request.user
        following = self.get_object()

        if request.method == 'DELETE':
            instance = user.following.filter(following=following)
            if not instance:
                raise serializers.ValidationError(
                    {
                        'errors': [
                            'You are not follower of this user.'
                        ]
                    }
                )

            instance.delete()

            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

        data = {
            'user': user.id,
            'following': id
        }

        subscription = FollowCreateSerializer(data=data)
        subscription.is_valid(raise_exception=True)
        subscription.save()
        serializer = self.get_serializer(following)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    @action(
        methods=['get'],
        serializer_class=FollowSerializer,
        detail=False,
    )
    def subscriptions(self, request):
        user = self.request.user

        def queryset():
            return User.objects.filter(
                subscriber__user=user
            )

        self.get_queryset = queryset
        return self.list(request)
