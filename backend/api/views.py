# # kittygram/cats/views.py
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status

# from recipes.models import Recipe
# from .serializers import RecipeSerializer

# @api_view(['GET', 'POST'])
# def recipe_list(request):
#     if request.method == 'POST':
#         serializer = RecipeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     recipes = Recipe.objects.all()
#     serializer = RecipeSerializer(recipes, many=True)
#     return Response(serializer.data)

# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def recipe_details(request, pk):
#     recipe = Recipe.objects.get(pk=pk)
#     if request.method == 'PUT' or request.method == 'PATCH':
#         serializer = RecipeSerializer(recipe, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         recipe.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     serializer = RecipeSerializer(recipe)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# from rest_framework import generics

# from recipes.models import Recipe
# from .serializers import RecipeSerializer

# class RecipeList(generics.ListCreateAPIView):
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeSerializer

# class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeSerializer

from rest_framework import viewsets

from api.serializers import (
    RecipeSerializer,
    AuthorSerialiser,
    TagSerializer,
    IngredientSerializer,
)
from recipes.models import (
    Recipe,
    Author,
    Tag,
    Ingredient,
)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerialiser


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
