from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from grocery_assistant.actions import create_or_delete_obj_use_func
from users.pagination import UsersPagination
from users.serializers import SimpleRecipeSerializer

from .filters import IngredientFilter, RecipeFilter
from .models import Favorite, Ingredient, Purchase, Recipe, Tag
from .permissions import AuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeGetSerializer, TagSerializer)

User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    pagination_class = UsersPagination

    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    AUTHENTICATED_ACTIONS = [
        'favorite', 'shopping_cart', 'download_shopping_cart'
    ]

    def get_queryset(self):
        return Recipe.objects.annotate_flags(self.request.user)

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
        recipe_id=self.kwargs['pk']

        serializer = SimpleRecipeSerializer(
            data=recipe_id,
            context={
                'request': request,
                'queryset': queryset,
                'error_msg_create': error_msg_create,
                'error_msg_delete': error_msg_delete
            }
        )
        return create_or_delete_obj_use_func(
            is_delete=(request.method == 'DELETE'),
            serializer=serializer,
            func={
                'create': queryset.create,
                'delete': queryset.filter(
                    user=self.request.user, recipe_id=recipe_id
                ).delete
            },
            args={
                'create': {'recipe_id': recipe_id, 'user': self.request.user},
                'delete': {}
            },
            msg_errors={
                'create': error_msg_create,
                'delete': error_msg_delete
            }
        )

    @action(['get'], detail=False)
    def download_shopping_cart(self, request, *args, **kwargs):
        cur_user = get_object_or_404(User, email=self.request.user)

        ingredients = Ingredient.objects.filter(
            amounts__recipe__shopping_cart__user=cur_user
        ).order_by('name').annotate(amount=Sum('amounts__amount'))

        content = []
        for ingredient in ingredients:
            m_u = ingredient.measurement_unit
            amount = ingredient.amount
            name = ingredient.name
            content.append(f'{name} ({m_u}) - {amount}')

        return HttpResponse('\r\n'.join(content), content_type='text/plain')
