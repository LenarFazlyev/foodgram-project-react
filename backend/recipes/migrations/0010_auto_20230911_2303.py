# Generated by Django 2.2.19 on 2023-09-11 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20230911_2259'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredientrecipe',
            options={'verbose_name': 'ингредиент/рецепт', 'verbose_name_plural': 'Ингредиенты/Рецепт'},
        ),
    ]