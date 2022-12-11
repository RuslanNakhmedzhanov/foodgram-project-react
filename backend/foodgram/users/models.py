from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель для пользователей."""

    email = models.EmailField(
        verbose_name='Email',
        max_length=20,
        unique=True)

    username = models.CharField(
        verbose_name='Логин',
        max_length=10,
        unique=True)

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=15)

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=20)

    password = models.CharField(
        verbose_name='Пароль',
        max_length=10)

    class Meta:
        ordering = ('id',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель для подписок."""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name='Подписчик',)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name='Подписка',)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [models.UniqueConstraint(name='unique_follows',
                                               fields=['user', 'author'],
                                               condition=None),
                       models.CheckConstraint(check=~models.Q(
                                              user=models.F('author')),
                                              name='non_follow')]

    def __str__(self):
        return f'Пользователь:{self.user.username}, подписан на: {self.author.username}'
