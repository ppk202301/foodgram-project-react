import ntpath
import os

from pathlib import Path

from django.conf import settings
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import get_template

from rest_framework import (
    serializers,
    status,
    viewsets,
)
from rest_framework.decorators import (
    action,
) 
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    SAFE_METHODS,
)
from rest_framework.response import Response

from .convert_to_pdf import Html_to_Pdf
from .filters import RecipeFilter
from .models import (
    Cart,
    Favorite,
    Ingredient,
    Ingredient_Recipe,
    Recipe,
    Tag,
)
from .paginator import RecipeCustomPaginator
from .permissions import (
    IsAuthor,
)
from .serializers import (
    CartSerializer,
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
            if self.action == 'download_shopping_cart':
                print(f'Debugging: work viewset get_permission return IsAuthenticated')
                return (
                    IsAuthenticated(),
                )

            print(f'Debugging: work viewset get_permission return AllowAny')
            return (
                AllowAny(),
            )

        if self.action in (
            'favorite',
            'shopping_cart',
        ):
            print(f'Debugging: work viewset get_permission return IsAuthenticated')
            return (
                IsAuthenticated(),
            )

        print(f'Debugging: work viewset get_permission return IsAuthenticated and IsAuthor')
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
            'delete',
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

        return  Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        methods=[
            'post',
            'delete',
        ],
        detail=True,
    )
    def shopping_cart(self, request, pk):
        print(f'Debugging: start shopping_cart')
        print(f'Debugging: start shopping_cart self = {self}')
        print(f'Debugging: start shopping_cart request = {request}')
        print(f'Debugging: start shopping_cart pk = {pk}')

        user = self.request.user
        recipe = self.get_object()

        print(f'Debugging: shopping_cart user = {user}')
        print(f'Debugging: shopping_cart recipe = {recipe}')

        if request.method == 'DELETE':

            print(f'Debugging: shopping_cart method == DELETE')

            existing_cart_recipe = Cart.objects.filter(
                recipe=recipe,
                user=user,
            )
            if not existing_cart_recipe:
                raise serializers.ValidationError(
                    {
                        'errors': [
                            ('This recipe is not found in '
                             'the user cart.')
                        ]
                    }
                )

            print(f'Debugging: shopping_cart method == instance  {existing_cart_recipe}')

            existing_cart_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        print(f'Debugging: shopping_cart method == POST')

        data = {
            'recipe': pk,
            'user': user.id,
        }
        new_cart_recipe = CartSerializer(
            data=data,
        )

        print(f'Debugging: shopping_cart new_cart_recipe = {new_cart_recipe}')

        new_cart_recipe.is_valid(
            raise_exception=True,
        )
        new_cart_recipe.save()

        serializer = RecipeMainInfoSerializer(recipe)

        print(f'Debugging: shopping serializer = {serializer}')

        return  Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        methods=[
            'get',
        ],
        detail=False,
    )
    def download_shopping_cart(self, request):
        user = self.request.user

        ingredients_to_buy = list(
            Ingredient_Recipe.objects.filter(
                recipe__carts__user=user
            )
            .values(
                'ingredient__id',
                'ingredient__name',
                'ingredient__measurement_unit',
            )
            .annotate(sum_amount=Sum('amount'))
            .order_by('ingredient__id')
        )

        html = (
            get_template('shoppyng_cart.html')
            .render(
                {'ingredients': ingredients_to_buy}
            )
        )

        font_path = '/fonts/DejaVuSansCondensed.ttf'

        print(f'Debugging: shopping font_path = {font_path}')
        print(f'Debugging: shopping font_path = {font_path}')

        font_path.replace(os.sep,ntpath.sep)

        print(f'Debugging: shopping after OS replace font_path = {font_path}')

        font_path_final = os.path.normpath(
                str(settings.STATIC_ROOT)
                + font_path
        )

        print(f'Debugging: shopping font_path_final = {font_path_final}')

        pdf3 = Html_to_Pdf()
        pdf3.add_font(
            'DejaVu',
            '',
            font_path_final,
        )
        pdf3.set_font(
            'DejaVu',
            '',
            10
        )
        pdf3.add_page()
        pdf3.write_html(html)

        return HttpResponse(
                bytes(pdf3.output()),
                content_type='application/pdf',
                status=status.HTTP_200_OK
            )
