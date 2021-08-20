from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import BooleanField, Value
from django.db.models.expressions import Exists, OuterRef

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField('Единицы измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)
    color = models.CharField('Цвет', max_length=200, unique=True)
    slug = models.SlugField('Короткая ссылка', unique=True, db_index=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class RecipeQuerySet(models.QuerySet):
    def annotate_flags(self, user):
        if user.is_anonymous:
            return self.annotate(
                is_favorited=Value(False, output_field=BooleanField()),
                is_in_shopping_cart=Value(False, output_field=BooleanField())
            )

        is_favorited = Favorite.objects.filter(
            recipe=OuterRef('pk'),
            user=user
        )
        is_in_shopping_cart = Purchase.objects.filter(
            recipe=OuterRef('pk'),
            user=user
        )
        return self.annotate(
            is_favorited=Exists(is_favorited),
            is_in_shopping_cart=Exists(is_in_shopping_cart)
        )


class RecipeManager(models.Manager):
    def get_queryset(self):
        return RecipeQuerySet(self.model, using=self._db)

    def annotate_flags(self, user):
        return self.get_queryset().annotate_flags(user)


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField('Название', max_length=200)
    image = models.ImageField("Фото блюда", upload_to='recipes')
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='recipes',
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes',
    )
    text = models.TextField('Описание')
    cooking_time = models.PositiveIntegerField(
        'Время приготовления в минутах',
        validators=[MinValueValidator(
            1, 'Время приготовления должно быть не менее минуты.'
        )]
    )
    objects = RecipeManager()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='amounts'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='ingredient_amount'
    )
    amount = models.PositiveIntegerField(
        'Количество',
        validators=[MinValueValidator(
            1, 'Количество ингредиента должно быть не менее единицы.'
        )]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_recipe_ingredient'
            )
        ]
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Человек, которому понравился рецепт',
        on_delete=models.CASCADE,
        related_name='fan'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorite_recipe'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite'
            )
        ]


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Покупатель',
        on_delete=models.CASCADE,
        related_name='customer'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_purchase'
            )
        ]
