from django.urls import (
    include,
    path,
)

from rest_framework.routers import DefaultRouter

from .views import (
    download_shopping_cart,
    IngredientViewSet,
    favorite,
    RecipeViewSet,
    shopping_cart,
    TagViewSet,
)


app_name = 'api'

router = DefaultRouter()

router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        download_shopping_cart,
        name='download_shopping_cart'
    ),
    path(
        'recipes/<int:recipe_id>/favorite/',
        favorite,
        name='favorite'
    ),
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        shopping_cart,
        name='shopping_cart'
    ),
    path('', include(router.urls)),
]
