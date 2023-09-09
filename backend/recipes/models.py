from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Название тэга', max_length=200)
    color = models.CharField('Цвет в HEX', max_length=7)
    slug = models.SlugField('Уникальный слаг', max_length=200 )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    pass

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
    title = models.CharField('Название блюда', max_length=50)
    # picture = models.ImageField(
    #     'Фото рецепта',
    #     upload_to='posts/',
    #     null=True,
    #     blank=True
    # )
    description = models.TextField('Описание рецепта')
    # ingredients = models.ManyToManyField(
    #     Ingredient,
    #     # on_delete=models.
    #     related_name='recipes',
    #     verbose_name='Ингридиенты'
    # )
    tag = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name='Теги'
    )
    cookingtime = models.IntegerField('Время приготовления в минутах')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.title}'
    
class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag}{self.recipe}'
