import ntpath
import os

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
)
from rest_framework.response import Response

from .convert_to_pdf import HtmlToPdf
from .filters import RecipeFilter
from .models import (
    Cart,
    Favorite,
    Ingredient,
    IngredientRecipe,
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
    pagination_class = None
    permission_classes = (
        AllowAny,
    )
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Ingredient Viewset"""
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (
        AllowAny,
    )
    queryset = Ingredient.objects.all().order_by('id')


class RecipeViewSet(viewsets.ModelViewSet):
    """Recipe Viewset"""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipeCustomPaginator
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        serializer = None
        if self.request.method == 'GET':
            serializer = RecipeSerializer
        elif self.request.method == 'PATCH':
            serializer = RecipeUpdateSerializer
        else:
            serializer = RecipeCreateSerializer
        return serializer

    def get_permissions(self):
        if self.request.method == 'GET':
            if self.action == 'download_shopping_cart':
                return (
                    IsAuthenticated(),
                )
            return (
                AllowAny(),
            )

        if self.action in (
            'favorite',
            'shopping_cart',
        ):
            return (
                IsAuthenticated(),
            )
        return (
            IsAuthenticated(),
            IsAuthor(),
        )

    def perform_create(self, serializer):
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
        user = self.request.user
        recipe = self.get_object()

        if request.method == 'DELETE':

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

            existing_fav_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        data = {
            'recipe': pk,
            'user': user.id,
        }
        new_favorite_recipe = FavoriteSerializer(
            data=data,
        )

        new_favorite_recipe.is_valid(
            raise_exception=True,
        )
        new_favorite_recipe.save()

        serializer = RecipeMainInfoSerializer(recipe)

        return Response(
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
        user = self.request.user
        recipe = self.get_object()

        if request.method == 'DELETE':
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

            existing_cart_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        data = {
            'recipe': pk,
            'user': user.id,
        }
        new_cart_recipe = CartSerializer(
            data=data,
        )

        new_cart_recipe.is_valid(
            raise_exception=True,
        )
        new_cart_recipe.save()

        serializer = RecipeMainInfoSerializer(recipe)

        return Response(
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
            IngredientRecipe.objects.filter(
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
        font_path.replace(
            os.sep,
            ntpath.sep
        )
        font_path_final = os.path.normpath(
            str(settings.STATIC_ROOT)
            + font_path
        )

        pdf3 = HtmlToPdf()
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
