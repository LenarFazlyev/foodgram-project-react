from datetime import datetime
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import permissions, status, viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin

from api.filters import RecipeFilter, IngredientFilter
from api.permissions import OwnerOrReadOnly
from api.serializers import (
    RecipeCreateSerializer,
    RecipeReadSerializer,
    TagSerializer,
    IngredientSerializer,
    CustomUserSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer,
    FollowSerializer,
)
from recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    Favorite,
    ShoppingCart,
    IngredientRecipe,
)

from users.models import (
    User,
    Follow,
)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(permissions.IsAuthenticated,),
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)

        if request.method == 'POST':
            serializer = FollowSerializer(
                author, data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        subscription = get_object_or_404(Follow, user=user, author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


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

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request):
        user = request.user
        if not user.shopping_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ingredients = (
            IngredientRecipe.objects.filter(
                recipe__shopping_cart__user=request.user
            )
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(cart_amount=Sum('amount'))
        )

        today = datetime.today()
        shopping_list = f'Ваш список покупок на: {today:%Y-%m-%d}\n\n'
        shopping_list += '\n'.join(
            [
                f'- {ingredient["ingredient__name"]} '
                f'({ingredient["ingredient__measurement_unit"]})'
                f' - {ingredient["cart_amount"]}'
                for ingredient in ingredients
            ]
        )

        filename = f'{user.username}_shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


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
            return Response('Объект удален', status=status.HTTP_204_NO_CONTENT)
        return Response(
            'Объект был уже удален либо не существует',
            status=status.HTTP_400_BAD_REQUEST,
        )


class ShoppingCartViewSet(DestroyModelMixin, CreateModelMixin, GenericViewSet):
    queryset = ShoppingCart.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ShoppingCartSerializer

    def create(self, request, *args, **kwargs):
        data = {'user': request.user.id, 'recipe': self.kwargs.get('id')}
        serializer = ShoppingCartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        obj = ShoppingCart.objects.filter(
            user_id=request.user.id, recipe_id=self.kwargs.get('id')
        )
        if obj:
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
