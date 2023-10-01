from rest_framework import (
    viewsets
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

from .models import (
    Ingredient,
    Recipe,
    Tag,
)
from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
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


class RecipeViewSet(viewsets.ModelViewSet):
    """Recipe Viewset"""
    queryset = Recipe.objects.all()
    http_method_names = [
        "delete",
        "get",
        "patch",
        "post",
    ]
    permission_classes = (
        IsAuthenticated,
    )

    def get_serializer_class(self):
        return RecipeSerializer