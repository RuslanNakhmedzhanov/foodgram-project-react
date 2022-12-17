from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import name_validator


class User(AbstractUser):
    """Класс пользователей"""

    username = models.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        verbose_name='Имя пользователя',
        unique=True,
        validators=[name_validator]
    )
    first_name = models.CharField(
        max_length=settings.NAME_MAX_LENGTH,
        verbose_name='Имя',
        validators=[name_validator]
    )
    last_name = models.CharField(
        max_length=settings.NAME_MAX_LENGTH,
        verbose_name='Фамилия',
        validators=[name_validator]
    )
    email = models.EmailField(
        max_length=settings.EMAIL_MAX_LENGTH,
        verbose_name='Email',
        unique=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Класс для подписки на авторов"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follow',
        verbose_name='Автор')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow'
            ),
            models.CheckConstraint(
                name='Ограничение на самоподписку',
                check=~models.Q(user=models.F('author')),
            ),
        ]

    def __str__(self):
        return f'{self.user} {self.author}'