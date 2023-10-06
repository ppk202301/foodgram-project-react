from rest_framework import (
    serializers,
    status,
    viewsets,
)
from rest_framework.decorators import (
    action,
    permission_classes,
) 
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    SAFE_METHODS,
)
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import (
    Cart,
    Favorite,
    Ingredient,
    Recipe,
    Tag,
)
from .paginator import RecipeCustomPaginator
from .permissions import (
    IsAuthor,
)
from .serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeCreateSerializer,
    RecipeMainInfoSerializer,
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
        print(f'Debugging: work viewset get_permission self.request.data = {self.request.data}')
        print(f'Debugging: work viewset get_permission self.request.query_params = {self.request.query_params}')
        print(f'Debugging: work viewset get_permission self.action = {self.action}')
        print(f'Debugging: work viewset get_permission self.request.method = {self.request.method}')

        if self.request.method == 'GET':
            return (
                AllowAny(),
            )
        if (self.action == 'favorite'
            or self.action == 'shopping_cart'):
            return (
                IsAuthenticated(),
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

    @action(
        methods=[
            'post',
            'delete'
        ],
        detail=True,
    )
    def favorite(self, request, pk):
        print(f'Debugging: start favorite')
        print(f'Debugging: start favorite self = {self}')
        print(f'Debugging: start favorite request = {request}')
        print(f'Debugging: start favorite pk = {pk}')

        user = self.request.user
        recipe = self.get_object()

        print(f'Debugging: favorite user = {user}')
        print(f'Debugging: favorite recipe = {recipe}')

        if request.method == 'DELETE':

            print(f'Debugging: favorite method == DELETE')

            existing_fav_recipe = Favorite.objects.filter(
                recipe=recipe,
                user=user,
            )
            if not existing_fav_recipe:
                raise serializers.ValidationError(
                    {
                        'errors': [
                            ('This recipe is not found in '
                             'the user favorite list.')
                        ]
                    }
                )

            print(f'Debugging: favorite method == instance  {existing_fav_recipe}')

            existing_fav_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        print(f'Debugging: favorite method == POST')

        data = {
            'recipe': pk,
            'user': user.id,
        }
        new_favorite_recipe = FavoriteSerializer(
            data=data,
        )

        print(f'Debugging: favorite new_favorite_recipe = {new_favorite_recipe}')

        new_favorite_recipe.is_valid(
            raise_exception=True,
        )
        new_favorite_recipe.save()

        serializer = RecipeMainInfoSerializer(recipe)

        print(f'Debugging: favorite serializer = {serializer}')

        return  Response(serializer.data, status=status.HTTP_201_CREATED)
