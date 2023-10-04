from django.db.models import Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.filters import RecipeFilter, IngredientFilter
from api.permissions import OwnerOrReadOnly
from api.serializers import (
    RecipeCreateSerializer,
    RecipeReadSerializer,
    TagSerializer,
    IngredientSerializer,
    UserSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer,
    FollowSerializer,
    FollowPostSerializer,
)
from recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    IngredientRecipe,
)

from users.models import User

from api.utils import create_shopping_list


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_permissions(self):
        if self.action == 'me':
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(permissions.IsAuthenticated,),
    )
    def subscribe(self, request, id):
        data = {'user': request.user.id, 'author': id}
        context = {"request": request}
        serializer = FollowPostSerializer(data=data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, **kwargs):
        subscription = request.user.follower.filter(
            author=self.kwargs.get('id')
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            'Такой подписки нет', status=status.HTTP_400_BAD_REQUEST
        )

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
    queryset = Recipe.objects.select_related('author').prefetch_related(
        'tags', 'ingredients'
    )
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeCreateSerializer

    @staticmethod
    def write_to_fav_or_subsc(serializer, pk, request):
        data = {'user': request.user.id, 'recipe': pk}
        context = {"request": request}
        serializer = serializer(data=data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(permissions.IsAuthenticated,),
    )
    def favorite(self, request, pk):
        return self.write_to_fav_or_subsc(FavoriteSerializer, pk, request)

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(permissions.IsAuthenticated,),
    )
    def shopping_cart(self, request, pk):
        return self.write_to_fav_or_subsc(ShoppingCartSerializer, pk, request)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        favorite = request.user.favorites.filter(recipe=pk)
        if favorite:
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            'Такого рецепта в избранном нет',
            status=status.HTTP_400_BAD_REQUEST,
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, **kwargs):
        shopping_cart = request.user.shoppingcarts.filter(
            recipe=self.kwargs.get('pk')
        )
        if shopping_cart:
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            'Такого рецепта в корзине нет', status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request):
        user = request.user
        if not user.shoppingcarts.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ingredients = (
            IngredientRecipe.objects.filter(
                recipe__shoppingcarts__user=request.user
            )
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(cart_amount=Sum('amount'))
            .order_by('ingredient__name')
        )
        shopping_list = create_shopping_list(ingredients)
        response = FileResponse(shopping_list, content_type='text/plain')
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
