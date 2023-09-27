from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        'Уникальный юзернейм',
        max_length=settings.MAX_LENGTH_CUSTOMED,
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=settings.MAX_LENGTH_EMAIL,
        unique=True,
    )
    password = models.CharField(
        'Пароль',
        max_length=settings.MAX_LENGTH_CUSTOMED,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        ordering = ('username', 'email',)
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name="Подписчик",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                name='unique_follow', fields=['user', 'author']
            ),
            models.CheckConstraint(
                name='no_follow_one_self',
                check=~models.Q(user=models.F('author')),
            ),
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
