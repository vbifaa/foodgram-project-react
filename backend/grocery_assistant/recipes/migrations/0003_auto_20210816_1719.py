# Generated by Django 3.1.7 on 2021-08-16 14:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20210811_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Время приготовления должно быть не менее минуты.')], verbose_name='Время приготовления в минутах'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Колличество ингредиента должно быть не менее еденицы.')], verbose_name='Количество'),
        ),
    ]
