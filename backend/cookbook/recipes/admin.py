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
        'recipe',
    )
    list_filter = (
        'user',
        'recipe',
    )
    search_fields = (
        'user',
        'recipe',
    )


class IngredientInline(admin.TabularInline):
    """Admin panel for Ingredient in Recipe model."""
    model = Ingredient_Recipe
    extra = 1
    min_num = 1
    list_display = (
        'recipe',
        'ingredient',
        'amount'
    )
    list_editable = (
        'recipe',
        'ingredient',
        'amount'
    )
    list_filter = (
        'recipe',
        'ingredient',
    )
    search_fields = (
        'recipe',
        'ingredient',
        'amount'
    )


class TagInLine(admin.TabularInline):
    """Admin panel for Recipe Tags model."""
    model = Recipe_Tag
    extra = 1
    min_num = 1
    list_display = (
        'recipe',
        'tag',
        'reg_date'
    )
    list_editable = (
        'recipe',
        'tag',
        'reg_date'
    )
    list_filter = (
        'recipe',
        'tag',
        'reg_date'
    )
    search_fields = (
        'recipe',
        'tag',
        'reg_date'
    )


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


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin panel for Recipe model."""
    inlines = (IngredientInline, TagInLine)
    list_display = (
        'id',
        'name',
        'text',
        'author',
        'pub_date',
        'cooking_time',
        'favorite_count',
        'image',
        'get_ingredients',
        'get_tags',
    )
    list_editable = (
        'text',
        'cooking_time',
    )
    list_filter = (
        'name',
        'author',
        'pub_date',
        'cooking_time',
    )
    search_fields = (
        'name',
        'author',
        'pub_date',
        'cooking_time',
    )
    readonly_fields = (
        'favorite_count',
    )

    inlines = (
        TagInLine,
        IngredientInline,
    )

    @admin.display(description='Favorites')
    def favorite_count(self, obj):
        return obj.favorites.count()

    def get_ingredients(self, obj):
        queryset = Ingredient_Recipe.objects.filter(
            recipe_id=obj.id
        ).all()
        return ', '.join(
            [f' {item.ingredient.name} {item.amount} '
             f'{item.ingredient.measurement_unit}'
             for item in queryset]
        )
    
    def get_tags(self, obj):
        queryset = Recipe_Tag.objects.filter(
            recipe_id=obj.id
        ).all()
        return ', '.join(
            [f' {item.tag.name} \n'
             for item in queryset]
        )
