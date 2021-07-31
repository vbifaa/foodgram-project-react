from django.urls import include, path 
from rest_framework import routers
from .views import IngredientViewSet, TagViewSet, RecipeViewSet

router = routers.DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes_api')
router.register('ingredients', IngredientViewSet, basename='ingredients_api')
router.register('tags', TagViewSet, basename='tags_api')


urlpatterns = [ 
    path('', include(router.urls))
]
