from django.contrib import admin

from .models import (
    Cart,
    Favorite,
    Ingredient,
    Ingredient_Recipe,
    Recipe,
    Recipe_Tag,
    Tag
)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin panel for Cart model."""
    list_display = (
        'user', 
        'recipe'
    )
    list_editable = (
        'recipe',
    )
    list_filter = (
        'user',
        'recipe'
    )
    search_fields = (
        'user',
        'recipe'
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Admin panel for Favotite model."""
    list_display = (
        'user', 
        'recipe'
    )
    list_editable = (
        'recipe',
    )
    list_filter = (
        'user',
        'recipe'
    )
    search_fields = (
        'user',
        'recipe'
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Admin panel for Ingredient model."""
    list_display = (
        'id',
        'name',
        'measurement_unit'
    )
    list_editable = (
        'measurement_unit',
    )
    list_filter = (
        'name',
        'measurement_unit'
    )
    search_fields = (
        'name',
        'measurement_unit'
    )


class IngredientInline(admin.TabularInline):
    """Admin panel for Ingredient in Recipe model."""
    model = Ingredient_Recipe
    list_display = (
        'recipe',
        'ingredient',
        'quantity'
    )
    list_editable = (
        'recipe',
        'ingredient',
        'quantity'
    )
    list_filter = (
        'recipe',
        'ingredient',
    )
    search_fields = (
        'recipe',
        'ingredient',
        'quantity'
    )


class TagInLine(admin.TabularInline):
    """Admin panel for Recipe Tags model."""
    model = Recipe_Tag
    list_display = (
        'recipe',
        'tag',
        'author',
        'reg_date'
    )
    list_editable = (
        'recipe',
        'tag',
        'author',
        'reg_date'
    )
    list_filter = (
        'recipe',
        'tag',
        'author',
        'reg_date'
    )
    search_fields = (
        'recipe',
        'tag',
        'author',
        'reg_date'
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin panel for Recipe model."""
    inlines = (IngredientInline, TagInLine)
    list_display = (
        'name',
        'text',
        'author',
        'pub_date',
        'production_time',
        'favorite_count',
    )
    list_editable = (
        'text',
        'production_time',
    )
    list_filter = (
        'name',
        'author',
        'pub_date',
        'production_time',
    )
    search_fields = (
        'name',
        'author',
        'pub_date',
        'production_time',
    )
    readonly_fields = (
        'favorite_count',
    )

    @admin.display(description='Favorites')
    def favorite_count(self, obj):
        return obj.favorites.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin panel for Tag model."""
    list_display = (
        'id',
        'name',
        'color',
        'slug'
    )
    list_editable = (
        'color',
        'slug'
    )
    list_filter = (
        'name',
        'color',
        'slug'
    )
    search_fields = (
        'name',
        'color',
        'slug'
    )
