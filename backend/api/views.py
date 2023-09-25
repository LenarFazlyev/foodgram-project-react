from djoser.views import UserViewSet
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import OwnerOrReadOnly
from api.serializers import (
    RecipeCreateSerializer,
    RecipeReadSerializer,
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
    serializer_class = RecipeCreateSerializer
    permission_classes = (OwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeReadSerializer
        return RecipeCreateSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    # permission_classes =


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    # permission_classes
    # нужно добавить фильтр для поиска по частичному вхождению в начале названия ингридиента
