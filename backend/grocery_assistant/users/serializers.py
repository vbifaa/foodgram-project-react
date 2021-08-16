from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from recipes.models import Recipe
from rest_framework import serializers
from django.db.models.query import QuerySet

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.BooleanField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def to_internal_value(self, data):
        return User.objects.get(id=data)

    def to_representation(self, instance):
        user = self.context['request'].user
        if isinstance(instance, QuerySet):
            instance = instance.annotate_flags(user)
        else:
            instance = User.objects.annotate_flags(user).get(id=instance.id)
        return super().to_representation(instance)


class SimpleRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    def to_internal_value(self, data):
        return Recipe.objects.get(id=data)

    def validate(self, recipe):
        recipe = super().validate(recipe)
        user = self.context['request'].user
        queryset = self.context['queryset']


        if self.context['request'].method == 'GET':
            self.create_validate(user=user, recipe=recipe, queryset=queryset)
        if self.context['request'].method == 'DELETE':
            self.delete_validate(user=user, recipe=recipe, queryset=queryset)
        return recipe

    def create_validate(self, user, recipe, queryset):
        if queryset.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                self.context['error_msg_create']
            )

    def delete_validate(self, user, recipe, queryset):
        if not queryset.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                self.context['error_msg_delete']
            )


class FollowingUsersSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        limit = self.context['request'].query_params.get('recipes_limit', None)
        recipes = obj.recipes.all()
        if limit is not None:
            recipes = recipes[:int(limit)]
        return SimpleRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def validate(self, author):
        attrs = super().validate(author)
        user = self.context['request'].user

        if self.context['request'].method == 'GET':
            self.create_validate(user=user, author=author)
        if self.context['request'].method == 'DELETE':
            self.delete_validate(user=user, author=author)
        return attrs

    def create_validate(self, user, author):
        if author == user:
            raise serializers.ValidationError(
                'Нельзя подписываться на самого себя.'
            )
        if author.following.filter(user=user).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя.'
            )

    def delete_validate(self, user, author):
        if author == user:
            raise serializers.ValidationError(
                'Нельзя отписываться от самого себя.'
            )
        if not author.following.filter(user=user).exists():
            raise serializers.ValidationError(
                'Вы не подписаны на этого пользователя.'
            )
