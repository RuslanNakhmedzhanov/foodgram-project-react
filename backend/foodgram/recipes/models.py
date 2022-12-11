from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User


class Tag(models.Model):
    """Модель тэгов."""

    BLUE = '#0000FF'
    GREEN = '#008000'
    RED = '#FF0000'

    COLOUR_CHOICES = [
        (BLUE, 'Синий'),
        (GREEN, 'Зеленый'),
        (RED, 'Красный'),
    ]

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название тега')

    colour = models.CharField(
        max_length=7,
        unique=True,
        choices=COLOUR_CHOICES,
        verbose_name='HEX color')

    slug = models.SlugField(
        max_length=10,
        unique=True,
        verbose_name='Имя слага')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return f'{self.name}'


class Ingredients(models.Model):
    """Модель для ингредиентов."""

    name = models.CharField(
        max_length=20,
        unique=True)

    measurement = models.CharField(
        verbose_name='Количество',
        max_length=5,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}'


class Recipes(models.Model):
    """Модель для рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор рецепта",
        related_name='recipe_author',)

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название рецепта')

    description = models.CharField(
        max_length=100,
        verbose_name='Описание')

    image = models.ImageField(
        'Изображение',
        upload_to='media/recipes/',)

    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientInRecipe',
        verbose_name='Ингредиенты',
        related_name='ingredient',
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name='tags')

    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(240)
        )
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}'


class RecipeTag(models.Model):
    """Модель для тэгов в рецепте."""

    recipe = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='recipe_tag'
    )
    tag = models.ForeignKey(
        Tag,
        verbose_name='Тэг',
        on_delete=models.CASCADE,
        related_name='tag_recipe'
    )

    class Meta:
        verbose_name = 'тэг в рецепте'
        verbose_name_plural = 'тэги в рецепте'
        ordering = ('-pk',)

    def __str__(self):
        return f'Тэг {self.tag.slug} рецепта {self.recipe.name}'


class IngredientInRecipe(models.Model):
    """Модель ингредиентов в рецепте."""

    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='recipe_ingredient')

    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredient_recipe')

    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(2500)
        )
    )

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredients', 'recipe'],
                name='unique ingredient in recipe')
        ]

    def __str__(self):
        return f'{self.ingredients}'


class Favorite(models.Model):
    """Модель для избранного."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        related_name='user_favorite')

    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_favorite')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite')
        ]

    def __str__(self):
        return f'Пользователь:{self.user.username}, рецепт: {self.recipe.name}'


class ShoppingCart(models.Model):
    """Модель для карты покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='cart_user'
    )
    recipe = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='cart_recipe'
    )

    class Meta:
        verbose_name = 'Карта покупок'
        verbose_name_plural = 'Карты покупок'
        ordering = ('-pk',)
        constraints = [
            models.UniqueConstraint(
                name='no_double_add_to_shopping_cart',
                fields=('user', 'recipe'),
            )
        ]

    def __str__(self):
        return (f'{self.recipe.name} в карте покупок пользователя {self.user.username}')
