import json
import os

from django.conf import settings
from django.core.management import BaseCommand

from pathlib import Path

from recipes.models import Ingredient


DATA_PATH = os.path.join(
    Path(settings.BASE_DIR).parent.parent,
    'data'
)
INGREDIENTS_DATA = os.path.join(
    DATA_PATH,
    'ingredients.json'
)


class Command(BaseCommand):
    """Import ingredients data from json file to the Database."""

    help = 'Import ingredients data from json file to the Database'

    def handle(self, *args, **kwargs):
        ingredients = ''

        try:
            with open(
                f'{os.path.normpath(INGREDIENTS_DATA)}',
                'r',
                encoding='UTF-8'
            ) as file:
                ingredients = json.load(file)
        except Exception as error:
            print(
                f'There is an error during I/O operation with '
                f'file {INGREDIENTS_DATA}. \n'
                f'Error: {error}.'
            )
            return

        for item in ingredients:
            try:
                Ingredient.objects.get_or_create(**item)
            except Exception as error:
                print(
                    f"Try to add ingredient {item['name']} to Database.\n"
                    f'Error: {error}.'
                )
                return

        print(
            f'Ingredients data has been imported into Database successfully.\n'
            f'Number of loaded items: {len(ingredients)}'
        )
