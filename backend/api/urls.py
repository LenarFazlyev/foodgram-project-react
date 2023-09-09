from django.urls import include, path
from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken import views

from .views import RecipeViewSet, AuthorViewSet, TagViewSet

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('authors', AuthorViewSet, basename='author')
router.register('tags', TagViewSet, basename='tags')

urlpatterns = [ 
    path('', include(router.urls)),
] 
