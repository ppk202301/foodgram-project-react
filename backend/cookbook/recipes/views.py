from rest_framework import (
    viewsets
)
from rest_framework.permissions import AllowAny

from .models import (
    Ingredient,
    Tag
)
from .serializers import (
    IngredientSerializer,
    TagSerializer
)

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Tag Viewset"""
    serializer_class = TagSerializer
    permission_classes = (
        AllowAny,
    )
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Ingredient Viewset"""
    serializer_class = IngredientSerializer
    permission_classes = (
        AllowAny,
    )
    queryset = Ingredient.objects.all().order_by('id')
