from rest_framework import serializers
import webcolors

from recipes.models import (
    Recipe,
    Author,
    Tag,
    TagRecipe,
    Ingredient,
    IngredientRecipe,
)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    # author = serializers.SlugRelatedField(
    #     # read_only=True,
    #     slug_field='first_name',
    # )
    tag = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = '__all__'
        # fields = ('id', 'author', 'title', 'description', 'cookingtime', 'tag')

    def create(self, validated_data):
        if 'tag' not in self.initial_data:
            recipe = Recipe.objects.create(**validated_data)
            return recipe
        tags = validated_data.pop('tag')
        recipe = Recipe.objects.create(**validated_data)

        for tag in tags:
            current_tag, status = Tag.objects.get_or_create(**tag)
            TagRecipe.objects.create(tag=current_tag, recipe=recipe)
        return recipe


class AuthorSerialiser(serializers.ModelSerializer):
    recipes = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Author
        fields = '__all__'
