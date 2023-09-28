from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from foodgram import constants
from users.models import User

MINTIME = MINQUANTITY = 1
MAXTIME = 600
MAXQUANTITY = 10000


class Tag(models.Model):
    name = models.CharField(
        'Название тэга',
        max_length=constants.MAX_LENGTH_FIELD,
        unique=True,
    )
    color = ColorField('Цвет в HEX', format='hex')
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=constants.MAX_LENGTH_FIELD,
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=constants.MAX_LENGTH_FIELD,
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=constants.MAX_LENGTH_FIELD,
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


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        'Название блюда',
        max_length=constants.MAX_LENGTH_FIELD,
    )
    image = models.ImageField(
        'Фото рецепта',
        upload_to='recipes/images',
    )
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
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах',
        validators=[
            MinValueValidator(
                MINTIME,
                message='Время приготовления должно быть больше 0',
            ),
            MaxValueValidator(
                MAXTIME,
                message=(
                    f'Время приготовления не может превышать {MAXTIME} минут'
                ),
            ),
        ],
    )
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
        related_name='recipe',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='tag',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'тэг/рецепт'
        verbose_name_plural = 'тэги/рецепты'
        constraints = [
            models.UniqueConstraint(
                name='unique_tag_recipe', fields=['tag', 'recipe']
            ),
        ]

    def __str__(self):
        return f'{self.tag}{self.recipe}'


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredientrecipes',
        on_delete=models.CASCADE,
        verbose_name='рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredientrecipes',
        on_delete=models.CASCADE,
        verbose_name='ингредиент',
    )
    amount = models.IntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                MINQUANTITY,
                message='Минимальное количество должно быть больше 0 г',
            ),
            MaxValueValidator(
                MAXQUANTITY,
                message=f'Максимальный вес не больше {MAXQUANTITY} г',
            ),
        ],
    )

    class Meta:
        verbose_name = 'ингредиент/рецепт'
        verbose_name_plural = 'Ингредиенты/Рецепт'

    def __str__(self):
        return f'{self.ingredient} in {self.recipe} with {self.amount}'


# Делали подобную на совместном проекте
class AbstractUserRelation(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='%(class)ss',
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='%(class)ss',
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                name='unique_user_relation',
                fields=['user', 'recipe'],
            ),
        ]


class Favorite(AbstractUserRelation):
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(AbstractUserRelation):
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'


# class Favorite(models.Model):
#     user = models.ForeignKey(
#         User,
#         related_name='favorites',
#         on_delete=models.CASCADE,
#         verbose_name='Пользователь',
#     )
#     recipe = models.ForeignKey(
#         Recipe,
#         related_name='favorites',
#         on_delete=models.CASCADE,
#         verbose_name='Рецепт',
#     )

#     class Meta:
#         verbose_name = 'Избранное'
#         verbose_name_plural = 'Избранное'
#         constraints = [
#             models.UniqueConstraint(
#                 name='unique_user_favorite', fields=['user', 'recipe']
#             ),
#         ]


# class ShoppingCart(models.Model):
#     user = models.ForeignKey(
#         User,
#         related_name='shopping_cart',
#         on_delete=models.CASCADE,
#         verbose_name='Пользователь',
#     )
#     recipe = models.ForeignKey(
#         Recipe,
#         related_name='shopping_cart',
#         on_delete=models.CASCADE,
#         verbose_name='Рецепт',
#     )

#     class Meta:
#         verbose_name = 'Корзина'
#         verbose_name_plural = 'Корзина'
#         constraints = [
#             models.UniqueConstraint(
#                 name='unique_user_shopping_cart', fields=['user', 'recipe']
#             ),
#         ]
