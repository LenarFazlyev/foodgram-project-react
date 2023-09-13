from rest_framework import serializers
from djoser.serializers import UserSerializer


from recipes.models import (
    Recipe,
    Author,
    Tag,
    TagRecipe,
    Ingredient,
    IngredientRecipe,
    User,
)


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        filds = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientrecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id',
        read_only=True,
    )
    name = serializers.PrimaryKeyRelatedField(
        source='ingredient.name',
        read_only=True,
    )
    measurement_unit = serializers.PrimaryKeyRelatedField(
        source='ingredient.measurement_unit',
        read_only=True,
    )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'amount',
            'measurement_unit',
        )


class RecipeSerializer(serializers.ModelSerializer):
    # author = serializers.SlugRelatedField(
    #     # read_only=True,
    #     slug_field='first_name',
    # )
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientrecipeSerializer(
        source='ingredient',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Recipe
        fields = '__all__'
        # fields = ('id', 'author', 'name', 'text', 'ingredients', 'tags')

    def create(self, validated_data):
        if 'tags' not in self.initial_data:
            recipe = Recipe.objects.create(**validated_data)
            return recipe
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        for tag in tags:
            current_tag, status = Tag.objects.get_or_create(**tag)
            TagRecipe.objects.create(tag=current_tag, recipe=recipe)
        return recipe


class RecipeListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='first_name',
    )
    tags = TagSerializer(
        many=True,
        required=False,
    )
    ingredients = IngredientrecipeSerializer(
        source='ingredient',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Recipe
        fields = '__all__'


class AuthorSerialiser(serializers.ModelSerializer):
    recipes = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Author
        fields = '__all__'
