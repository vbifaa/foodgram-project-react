from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from users.pagination import UsersPagination
from users.serializers import SimpleRecipeSerializer

from .filters import RecipeFilter
from .models import Favorite, Ingredient, Purchase, Recipe, Tag
from .permissions import AuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeGetSerializer, TagSerializer)

User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = UsersPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = RecipeFilter

    AUTHENTICATED_ACTIONS = [
        'favorite', 'shopping_cart', 'download_shopping_cart'
    ]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeGetSerializer
        return RecipeCreateSerializer

    def get_permissions(self):
        if (
            self.action in self.AUTHENTICATED_ACTIONS
            or self.request.method == 'POST'
        ):
            return (permissions.IsAuthenticated(),)
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (AuthorOrReadOnly(),)

    @action(['get', 'delete'], detail=True)
    def favorite(self, request, *args, **kwargs):
        return self.create_delete_relation(
            request=request,
            queryset=Favorite.objects,
            error_msg_create='Рецепт уже в списке избранных.',
            error_msg_delete='Рецепт не в списке избранных.'
        )

    @action(['get', 'delete'], detail=True)
    def shopping_cart(self, request, *args, **kwargs):
        return self.create_delete_relation(
            request=request,
            queryset=Purchase.objects,
            error_msg_create='Рецепт уже в списке покупок.',
            error_msg_delete='Рецепт не в списке покупок.'
        )

    def create_delete_relation(
        self, request, queryset, error_msg_create, error_msg_delete
    ):
        cur_user = get_object_or_404(User, email=self.request.user)
        recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])
        obj = queryset.filter(user=cur_user, recipe=recipe)

        if request.method == 'GET':
            return self.create_relation(
                cur_user=cur_user,
                recipe=recipe,
                obj=obj,
                queryset=queryset,
                error_msg=error_msg_create
            )
        return self.delete_relation(
            obj=obj,
            error_msg=error_msg_delete
        )

    def create_relation(self, cur_user, recipe, obj, queryset, error_msg):
        if obj.exists():
            return self.bad_400_request(error_msg)

        queryset.create(user=cur_user, recipe=recipe)
        serializer = SimpleRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_relation(self, obj, error_msg):
        if not obj.exists():
            return self.bad_400_request(error_msg)

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def bad_400_request(self, error_msg):
        return Response(
                {'errors': error_msg},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(['get'], detail=False)
    def download_shopping_cart(self, request, *args, **kwargs):
        cur_user = get_object_or_404(User, email=self.request.user)

        ingredients = Ingredient.objects.filter(
            amounts__recipe__author=cur_user
        ).order_by('name').annotate(amount=Sum('amounts__amount'))

        content = ''
        for ingredient in ingredients:
            m_u = ingredient.measurement_unit
            amount = str(ingredient.amount)
            name = ingredient.name
            content += name + ' (' + m_u + ') - ' + amount + '\n'

        return HttpResponse(content, content_type='text/plain')
