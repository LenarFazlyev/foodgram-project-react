# Generated by Django 3.2.16 on 2023-10-04 18:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0020_auto_20230929_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Минимальное количество должно быть больше 0 г'), django.core.validators.MaxValueValidator(10000, message=('Максимальный вес не больше', '10000 г'))], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Время приготовления должно быть больше 0'), django.core.validators.MaxValueValidator(600, message=('Время приготовления не может превышать', 'f{constants.MAXTIME} минут'))], verbose_name='Время приготовления в минутах'),
        ),
    ]