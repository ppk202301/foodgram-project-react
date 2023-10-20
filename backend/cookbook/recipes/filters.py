from django_filters import rest_framework as filters

from .models import (
    Recipe,
    Tag,
)


class RecipeFilter(filters.FilterSet):
    """Filter for recipes."""
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_in_shopping_cart = filters.NumberFilter(
        field_name='carts__user',
        method='filter_items_for_user',
    )
    is_favorited = filters.NumberFilter(
        field_name='favorites__user',
        method='filter_items_for_user',
    )

    class Meta:
        model = Recipe
        fields = (
            'author',
        )

    def filter_items_for_user(self, queryset, name, value):
        user = self.request.user

        if user.is_anonymous or not int(value):
            return queryset
        return queryset.filter(**{name: user})
