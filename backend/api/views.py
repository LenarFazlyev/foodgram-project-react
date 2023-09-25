from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import permissions, status, viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin

from api.filters import RecipeFilter
from api.permissions import OwnerOrReadOnly
from api.serializers import (
    RecipeCreateSerializer,
    RecipeReadSerializer,
    TagSerializer,
    IngredientSerializer,
    CustomUserSerializer,
    FavoriteSerializer,
)
from recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    Favorite,
)

from users.models import (
    User,
    Follow,
)



class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
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


class FavoriteViewSet(DestroyModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Favorite.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FavoriteSerializer

    def create(self, request, *args, **kwargs):
        data = {'user': request.user.id, 'recipe': self.kwargs.get('id')}
        serializer = FavoriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        obj = Favorite.objects.filter(
            user_id=request.user.id, recipe_id=self.kwargs.get('id')
        )
        if obj:
            obj.delete()
            return Response('Объект удален',status=status.HTTP_204_NO_CONTENT)
        return Response('Объект был уже удален либо не существует',status=status.HTTP_400_BAD_REQUEST)
