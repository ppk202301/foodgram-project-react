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
from .paginator import FollowCustomPaginator

class UserViewSet(UserViewSet):
    """User Viewset"""
    @action(
        methods=['post', 'delete'], 
        serializer_class=FollowSerializer,
        detail=True,
    )
    def subscribe(self, request, id):
        following = self.get_object()
        user = self.request.user

        if request.method == 'DELETE':
            instance = user.follower.filter(following=following)

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
            'following': id,
        }

        new_follow = FollowCreateSerializer(data=data)
        new_follow.is_valid(raise_exception=True)
        new_follow.save()
        serializer = self.get_serializer(following)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
    
    @action(
        methods=['get'],
        serializer_class=FollowSerializer,
        pagination_class = FollowCustomPaginator,
        detail=False,
    )
    def subscriptions(self, request):
        user = self.request.user

        def queryset():
            return User.objects.filter(id__in=list(user.following.all().values_list('user_id', flat=True)))

        self.get_queryset = queryset

        return self.list(request)
