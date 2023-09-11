from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Название тэга', max_length=200)
    color = models.CharField('Цвет в HEX', max_length=7)
    slug = models.SlugField('Уникальный слаг', max_length=200)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField("Название", max_length=200)
    measurement_unit = models.CharField(
        "Единицы измерения",
        max_length=200,
    )

    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} - {self.measurement_unit}'


class Author(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# подправь picture и on_delete
class Recipe(models.Model):
    author = models.ForeignKey(
        Author,
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
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.tag}{self.recipe}'


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredientrecipe',
        on_delete=models.CASCADE,
        verbose_name='рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredientrecipe',
        on_delete=models.CASCADE,
        verbose_name='ингредиент'
    )
    amount = models.IntegerField('Количество')

    class Meta:
        verbose_name = 'ингредиент/рецепт'
        verbose_name_plural = 'Ингредиенты/Рецепт'        

    def __str__(self):
        return f'{self.ingredient}{self.recipe}'
