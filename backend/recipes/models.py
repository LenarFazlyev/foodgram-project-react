from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    pass


class Ingredient(models.Model):
    pass


# подправь picture и on_delete
class Recipe(models.Model):
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='recipes',
    #     verbose_name='Автор',
    # )
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
    # tags = models.ManyToManyField(
    #     Tag,
    #     # on_delete=
    #     related_name='recipes',
    #     verbose_name='Теги'
    # )
    cookingtime = models.IntegerField('Время приготовления в минутах')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.title}'
