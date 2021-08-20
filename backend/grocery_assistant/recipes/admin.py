from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_display_links = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name',)
    list_display_links = ('name',)


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'author', 'name', 'get_tags', 'image', 'text', 'cooking_time'
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('author', 'tags',)
    inlines = [
        IngredientInline
    ]

    def get_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])

    get_tags.short_description = 'Теги'


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'ingredient', 'recipe', 'amount'
    )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
