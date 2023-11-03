import ntpath
import os

from django.conf import settings
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template

from rest_framework import (
    status,
    viewsets,
)
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response

from .convert_to_pdf import HtmlToPdf
from .filters import RecipeFilter
from recipes.models import (
    Cart,
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    Tag,
)
from recipes.paginator import RecipeCustomPaginator
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
        if self.request.method == 'GET':
            return RecipeSerializer
        if self.request.method == 'PATCH':
            return RecipeUpdateSerializer
        return RecipeCreateSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return AllowAny()

        return (
            IsAuthenticated(),
            IsAuthor(),
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )


@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def shopping_cart(request, recipe_id):
    """Manage shopping Cart"""
    user = request.user

    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
    )

    if request.method == "DELETE":
        Cart.objects.filter(
            user=user,
            recipe=recipe,
        ).delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    data = {
        'recipe': recipe_id,
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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_shopping_cart(request):
    """Create PDF file of ingredients in the shopping cart"""
    user = request.user

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


@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def favorite(request, recipe_id):
    """Manage Favorite"""
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
    )
    user = request.user

    if request.method == "DELETE":
        Favorite.objects.filter(
            user=user,
            recipe=recipe,
        ).delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    data = {
        'recipe': recipe_id,
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
        status=status.HTTP_201_CREATED
    )
