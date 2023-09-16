from rest_framework import viewsets
from djoser.serializers import UserSerializer
from djoser.views import UserViewSet

from api.serializers import (
    RecipeSerializer,
    RecipeListSerializer,
    TagSerializer,
    IngredientSerializer,
    CustomUserSerializer,
)
from recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    User,
)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeListSerializer
        return RecipeSerializer



class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

