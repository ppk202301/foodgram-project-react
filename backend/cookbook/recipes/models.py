from typing import Final

from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models

from users.models import User

MAX_SLUG_NAME_LENGTH: Final[int] = 250
MIN_AMOUNT: Final[float] = 0.001
MIN_COOKING_TIME: Final[int] = 1


class Ingredient(models.Model):
    """Ingredient model"""
    name = models.CharField(
        max_length=250,
        verbose_name='ingredient name',
        help_text='Could not be empty.'
    )
    measurement_unit = models.CharField(
        max_length=30,
        verbose_name='ingredient unit',
        help_text='Could not be empty.'
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient_unit'
            )
        ]
        ordering = ['name']

    def __str__(self):
        return (
            f'Ingredient: {self.name}, '
            f'unit: {self.measurement_unit}'
        )


class Tag(models.Model):
    """Tag model."""
    name = models.CharField(
        max_length=250,
        unique=True,
        verbose_name='Tag name',
        help_text='Could not be empty. Must be unique.'
    )
    color = ColorField(
        max_length=50,
        unique=True,
        verbose_name='Tag color HEX code.',
        help_text='Could not be empty. Must be unique.'
    )
    slug = models.SlugField(
        max_length=MAX_SLUG_NAME_LENGTH,
        unique=True,
        verbose_name='Tag slag.',
        help_text='Could not be empty. Must be unique.'
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']

    def __str__(self):
        return f'Tag: {self.name}'


class Recipe(models.Model):
    """Recipe model."""
    name = models.CharField(
        max_length=250,
        unique=True,
        verbose_name='Recipe title',
        help_text='Name your recipe.'
    )
    image = models.ImageField(
        upload_to='recipes/image',
        verbose_name='Recipe image',
        help_text='Show the final result.'
    )
    text = models.TextField(
        max_length=250,
        blank=True,
        verbose_name='Description',
        help_text='Describe your recipe.'
    )
    cooking_time = models.PositiveIntegerField(
        default=1,
        verbose_name='Recipe production time',
        help_text=(
            f'Estimate approximate production time '
            f'in minutes (min {MIN_COOKING_TIME}).',
        ),
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME,
                f'Production time should be more than {MIN_COOKING_TIME} min.'
            )
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date of publication'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Author',
        related_name='recipes',
        help_text='Point the recipe author.'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Recipe ingregiemts',
        related_name='recipes',
        help_text='Add all components to your dish.'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Recipe tags',
        help_text='Add all tags to your recipe.'
    )

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['-pub_date']

    def __str__(self):
        return (
            f'Recipe: {self.id}. {self.name}, '
            f'author: {self.author}'
        )


class Cart(models.Model):
    """Cart model."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Recipe in the cart',
        help_text='Point the ordered recipe.'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='buyers',
        verbose_name='Buyer',
        help_text='Point the buyer.'
    )

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='no_dublicated_recipes_in_cart'
            )
        ]


class Favorite(models.Model):
    """User favorite recipes model."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Favorite recipe',
        help_text='Point a favorite recipe.'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='User who has the favorite recipe',
        help_text='Point the recipe fan.'
    )

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='no_dublicated_favorite_pairs'
            )
        ]


class IngredientRecipe(models.Model):
    """Ingredient in Recipe model."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Ingredient',
        help_text='One of recipe ingredients.'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Recipe',
        help_text='Ingredient is a part of this recipe.'
    )
    amount = models.FloatField(
        default=MIN_AMOUNT,
        verbose_name='quantity',
        help_text='Ingredient amount in the recipe (min 0.001).',
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                f'Min value should be more than {MIN_AMOUNT}.'
            ),
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='no_duplicated_ingredients_in_recipe'
            )
        ]

    def __str__(self):
        return (
            f'Recipe {self.recipe.id}, {self.recipe.name} has '
            f'ingredient {self.ingredient.name} in '
            f'amount {self.amount} of '
            f'{self.ingredient.measurement_unit}'
        )


class RecipeTag(models.Model):
    """Tags of Recipe model."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes_tags',
        verbose_name='Recipe',
        help_text='One of recipes.'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tags_recipes',
        verbose_name='Tag',
        help_text='One of recipe tags.'
    )
    reg_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date of registration'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='no _duplicated_tags_for_recipe'
            )
        ]
        ordering = ['-reg_date']

    def __str__(self):
        return (
            f'Recipe {self.recipe.name} has '
            f'tag {self.tag.name} '
            f'added on {self.reg_date}'
        )
