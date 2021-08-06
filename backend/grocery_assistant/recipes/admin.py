from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name',)


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'author', 'name', 'image', 'text', 'cooking_time'
    )
    filter_horizontal = ('ingredients', 'tags',)
    search_fields = ('name',)
    list_filter = ('author', 'tags',)
    inlines = [
        IngredientInline,
    ]


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'ingredient', 'recipe', 'amount'
    )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
