from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from users.serializers import CustomUserSerializer

from .models import Ingredient, Recipe, RecipeIngredient, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")

    def to_internal_value(self, data):
        return get_object_or_404(Ingredient, id=data)


class IngredientWithAmountSerializer(serializers.Serializer):
    id = IngredientSerializer()
    amount = serializers.IntegerField(min_value=1)


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientWithAmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    image = Base64ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = (
            'tags', 'ingredients', 'name', 'image', 'text', 'cooking_time'
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        validated_data['author'] = self.context['request'].user

        if 'recipe' in validated_data:
            recipe = validated_data.pop('recipe')
            Recipe.objects.filter(id=recipe.id).update(**validated_data)
        else:
            recipe = Recipe.objects.create(**validated_data)

        recipe.tags.set(tags)

        for ingredient in ingredients:
            RecipeIngredient.objects.get_or_create(
                ingredient=ingredient['id'],
                recipe=recipe,
                amount=ingredient['amount'],
            )

        return recipe

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        validated_data['recipe'] = instance
        return self.create(validated_data)

    def to_representation(self, instance):
        read_serializer = RecipeGetSerializer()
        read_serializer.context['request'] = self.context['request']
        return read_serializer.to_representation(instance)


class RecipeGetSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_ingredients(self, obj):
        res = []

        for ingredient in obj.ingredients.all():
            amount = get_object_or_404(
                RecipeIngredient, recipe=obj, ingredient=ingredient
            ).amount
            res.append({
                    'id': ingredient.id,
                    'name': ingredient.name,
                    'measurement_unit': ingredient.measurement_unit,
                    'amount': amount
                }
            )
        return res

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return (
            not user.is_anonymous
            and obj.favorite_recipe.filter(user=user).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return (
            not user.is_anonymous
            and obj.shopping_cart.filter(user=user).exists()
        )
