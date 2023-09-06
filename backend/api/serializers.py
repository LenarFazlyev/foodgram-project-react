# from rest_framework import serializers

# from recipes.models import Recipe

# class RecipeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Recipe
#         fields = 'title'

from rest_framework import serializers

from recipes.models import Recipe, Author


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='first_name',
    )

    class Meta:
        model = Recipe
        # fields = '__all__' 
        fields = ('author', 'title', 'description', 'cookingtime') 


class AuthorSerialiser(serializers.ModelSerializer):
    recipes = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('first_name', 'recipes')