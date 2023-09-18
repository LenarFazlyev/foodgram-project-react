from colorfield.fields import ColorField
from django.conf import settings
from django.db import models
from users.models import User


# User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Название тэга',
        max_length=settings.MAX_LENGTH_FIELD_200,
        unique=True,
    )
    color = ColorField(
        'Цвет в HEX',
        format="hexa",
        max_length=7,
    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=settings.MAX_LENGTH_FIELD_200,
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        "Название",
        max_length=settings.MAX_LENGTH_FIELD_200,
    )
    measurement_unit = models.CharField(
        "Единицы измерения",
        max_length=settings.MAX_LENGTH_FIELD_200,
    )

    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                name='unique_name_measurement',
                fields=['name', 'measurement_unit'],
            )
        ]

    def __str__(self):
        return f'{self.name} - {self.measurement_unit}'


# подправь picture и on_delete
class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField('Название блюда', max_length=200)
    # picture = models.ImageField(
    #     'Фото рецепта',
    #     upload_to='posts/',
    #     null=True,
    #     blank=True
    # )
    text = models.TextField('Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='IngredientRecipe',
        verbose_name='Ингридиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        through='TagRecipe',
        verbose_name='Теги',
    )
    cooking_time = models.IntegerField('Время приготовления в минутах')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}'


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        verbose_name='Тег',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'тэг/рецепт'
        verbose_name_plural = 'тэги/рецепты'
        constraints = [
            models.UniqueConstraint(
                name='unique_tag', fields=['tag', 'recipe']
            ),
        ]

    def __str__(self):
        return f'{self.tag}{self.recipe}'


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredient',
        on_delete=models.CASCADE,
        verbose_name='рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipe',
        on_delete=models.CASCADE,
        verbose_name='ингредиент',
    )
    amount = models.IntegerField('Количество')

    class Meta:
        verbose_name = 'ингредиент/рецепт'
        verbose_name_plural = 'Ингредиенты/Рецепт'

    def __str__(self):
        return f'{self.ingredient}{self.recipe}'
