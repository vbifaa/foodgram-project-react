import django_filters as filters
from django_filters.widgets import BooleanWidget

from .models import Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    is_favorited = filters.BooleanFilter(
        method='filter_favorite', widget=BooleanWidget()
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart',
        widget=BooleanWidget()
    )

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def filter_favorite(self, queryset, name, value):
        user = self.request.user
        if value:
            return Recipe.objects.filter(favorite_recipe__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return Recipe.objects.filter(shopping_cart__user=user)
        return queryset
