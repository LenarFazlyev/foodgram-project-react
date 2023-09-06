from django.urls import include, path
from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken import views

from .views import RecipeViewSet, AuthorViewSet

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('authors', AuthorViewSet, basename='author')

urlpatterns = [ 
    path('', include(router.urls)),
] 
