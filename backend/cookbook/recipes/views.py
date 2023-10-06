from rest_framework import (
    status,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    SAFE_METHODS,
)

from .filters import RecipeFilter
from .models import (
    Ingredient,
    Recipe,
    Tag,
)
from .paginator import RecipeCustomPaginator
from .permissions import (
    IsAuthor,
)
from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
    RecipeCreateSerializer,
    RecipeUpdateSerializer,
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

    print(f'Debugging: work RecipeViewSet')

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipeCustomPaginator
    filterset_class = RecipeFilter

    def get_serializer_class(self):

        print(f'Debugging: work viewset get_serializer_class')

        if self.request.method == 'GET':
            return RecipeSerializer
        elif self.request.method == 'PATCH':
            return RecipeUpdateSerializer
        return RecipeCreateSerializer

    def get_permissions(self):

        print(f'Debugging: work viewset get_permission')

        if self.request.method == 'GET':
            return (
                AllowAny(),
            )
        return (
            IsAuthenticated(),
            IsAuthor(),
        )

    def perform_create(self, serializer):

        print(f'Debugging: perform_create')
        print(f'Debugging: perform_create serializer = {serializer}')

        serializer.save(
           author=self.request.user
        )
