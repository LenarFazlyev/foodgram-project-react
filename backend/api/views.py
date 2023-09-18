from djoser.views import UserViewSet
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import OwnerOrReadOnly
from api.serializers import (
    # RecipeSerializer,
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


class CustomUserViewSet(viewsets.ModelViewSet):
    # class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    # permission_classes = (OwnerOrReadOnly,)

    # @action(detail=True, url_path='me')
    # def get_me(
    # self,
    # request,
    # ):
    # me = User.objects.get(pk=request.pk)
    # serializer = self.get_serializer(me, many=True)
    # return Response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    # serializer_class = RecipeSerializer
    serializer_class = RecipeListSerializer

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return RecipeListSerializer
    #     return RecipeSerializer


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
