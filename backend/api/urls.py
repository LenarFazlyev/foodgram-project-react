from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    RecipeViewSet,
    TagViewSet,
    IngredientViewSet,
    CustomUserViewSet,
    FavoriteViewSet,
)

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register(
    'recipes/(?P<id>[^/.]+)/favorite',
    FavoriteViewSet,
    basename='favorite'
)
router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
