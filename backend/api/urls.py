from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    RecipeViewSet,
    AuthorViewSet,
    TagViewSet,
    IngredientViewSet
)

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('authors', AuthorViewSet, basename='authors')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
