from rest_framework import (
    viewsets
)
from rest_framework.permissions import AllowAny

from .models import (
    Tag
)
from .serializers import (
    TagSerializer
)

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """User Viewset"""
    serializer_class = TagSerializer
    permission_classes = (
        AllowAny,
    )
    queryset = Tag.objects.all()

