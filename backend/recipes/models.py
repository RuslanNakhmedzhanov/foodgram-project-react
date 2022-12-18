from django.conf import settings
from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from users.validators import name_validator

User = get_user_model()


class Tag(models.Model):
    """Класс тегов"""

    name = models.CharField(
        verbose_name='Тег',
        max_length=settings.NAME_MAX_LENGTH,
        unique=True,
        validators=[name_validator]
    )
    color = ColorField(
        verbose_name='Hex-цвет',
        max_length=7,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='slug',
        max_length=settings.SLUG_MAX_LENGTH,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return f'{self.name}, {self.slug}, цвет: {self.color}'


class Ingredient(models.Model):
    """Класс ингредиентов"""

    name = models.CharField(
        max_length=settings.NAME_MAX_LENGTH,
        verbose_name='Название',
        validators=[name_validator]
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единицы измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Класс рецептов"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        verbose_name='Название блюда',
        max_length=200)
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='recipe/')
    text = models.TextField(
        verbose_name='Описание блюда')
    ingredients = models.ManyToManyField(
        "IngredientRecipe",
        related_name='recipes',
        verbose_name='Ингредиенты блюда',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            1, 'Время приготовления блюда должно быть больше 0',
        )],
        verbose_name='Время приготовления'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return f'{self.author.email}, {self.name}'


class IngredientRecipe(models.Model):
    """Вспомогательный класс, связывающий ингредиенты и рецепты"""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            1, 'Количество должно быть больше 0',
        )],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return f'{self.ingredient}'


class Favorite(models.Model):
    """Класс избранное"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='+'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorites',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingList(models.Model):
    """Вспомогательный класс для формирования списка покупок"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shop_list',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='+'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_shoppingList'
            ),
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'
