from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from users.pagination import UsersPagination
from users.serializers import SimpleRecipeSerializer

from .filters import RecipeFilter
from .models import (Favorite, Ingredient, Purchase, Recipe, RecipeIngredient,
                     Tag)
from .permissions import AuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeGetSerializer, TagSerializer)

User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = UsersPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeGetSerializer
        return RecipeCreateSerializer

    def get_permissions(self):
        if (
            (
                self.action == 'favorite' or 'shopping_cart' or
                'download_shopping_cart'
            )
            or self.request.method == 'POST'
        ):
            return (permissions.IsAuthenticated(),)
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (AuthorOrReadOnly(),)

    @action(['get', 'delete'], detail=True)
    def favorite(self, request, *args, **kwargs):
        cur_user = get_object_or_404(User, email=self.request.user)
        recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])
        favorite = Favorite.objects.filter(user=cur_user, recipe=recipe)

        create_wrong = request.method == 'GET' and favorite.exists()
        delete_wrong = request.method == 'DELETE' and not favorite.exists()

        if create_wrong or delete_wrong:
            if create_wrong:
                error = 'Рецепт уже в списке избранных.'
            else:
                error = 'Рецепт не в списке избранных.'
            return Response(
                {
                    'errors': error
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if self.request.method == 'GET':
            Favorite.objects.create(user=cur_user, recipe=recipe)
            serializer = SimpleRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['get', 'delete'], detail=True)
    def shopping_cart(self, request, *args, **kwargs):
        cur_user = get_object_or_404(User, email=self.request.user)
        recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])
        purchase = Purchase.objects.filter(user=cur_user, recipe=recipe)

        create_wrong = request.method == 'GET' and purchase.exists()
        delete_wrong = request.method == 'DELETE' and not purchase.exists()

        if create_wrong or delete_wrong:
            if create_wrong:
                error = 'Рецепт уже в списке покупок.'
            else:
                error = 'Рецепт не в списке покупок.'
            return Response(
                {
                    'errors': error
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if self.request.method == 'GET':
            Purchase.objects.create(user=cur_user, recipe=recipe)
            serializer = SimpleRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            purchase.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['get'], detail=False)
    def download_shopping_cart(self, request, *args, **kwargs):
        cur_user = get_object_or_404(User, email=self.request.user)
        recipes = Recipe.objects.filter(shopping_cart__user=cur_user)
        print(recipes)

        ingredients = {}
        for recipe in recipes:
            for ingredient in recipe.ingredients.all():
                amount = get_object_or_404(
                    RecipeIngredient, recipe=recipe, ingredient=ingredient
                ).amount

                if ingredient.name in ingredients:
                    ingredients[ingredient.name]['amount'] += amount
                else:
                    ingredients[ingredient.name] = {
                        'amount': amount,
                        'measurement_unit': ingredient.measurement_unit
                    }

        content = ''
        for name, info in ingredients.items():
            m_u = info['measurement_unit']
            amount = str(info['amount'])
            content += name + ' (' + m_u + ') - ' + amount + '\n'

        return HttpResponse(content, content_type='text/plain')
