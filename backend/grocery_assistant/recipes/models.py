from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField('Единицы измерения', max_length=200)


class Tag(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)
    color = models.CharField('Цвет', max_length=200, unique=True)
    slug = models.SlugField('Короткая ссылка', unique=True, db_index=True)


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    name = models.CharField('Название', max_length=200)
    image = models.ImageField(verbose_name="Фото блюда", upload_to='recipes')
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингридиент',
        related_name='recipes',
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes',
    )
    text = models.TextField('Описание')
    cooking_time = models.PositiveIntegerField('Время приготовления в минутах')


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, blank=False, related_name='amounts'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, blank=False
    )
    amount = models.PositiveIntegerField('Количество', blank=False)

    class Meta:
        unique_together = ['ingredient', 'recipe']


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        related_name='fan'
    )
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE,
        blank=False,
        related_name='favorite_recipe'
    )

    class Meta:
        unique_together = ['user', 'recipe']


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        related_name='customer'
    )
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE,
        blank=False,
        related_name='shopping_cart'
    )

    class Meta:
        unique_together = ['user', 'recipe']
