# Generated by Django 4.2.1 on 2023-10-04 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_remove_recipe_tag_author_alter_recipe_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient_recipe',
            old_name='quantity',
            new_name='amount',
        ),
    ]
