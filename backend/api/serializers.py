from rest_framework import serializers
from djoser.serializers import UserSerializer


from recipes.models import (
    Recipe,
    Tag,
    TagRecipe,
    Ingredient,
    IngredientRecipe,
)
from users.models import User, Follow


# class CustomUserSerializer(UserSerializer):
class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):
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


class IngredientRecipeCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    # id = serializers.IntegerField()
    # amount = serializers.IntegerField()
    # id = serializers.PrimaryKeyRelatedField(
    #     source='ingredient.id',
    #     read_only=True,
    # )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'amount',
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    ingredients = IngredientRecipeCreateSerializer(
        source='ingredient_recipe',
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    # tags = TagSerializer(
    #     many=True,
    #     read_only=True,
    #     required = False,
    # )
    #     ingredients = IngredientrecipeSerializer(
    #         source='ingredient',
    #         many=True,
    #         read_only=True,
    #     )

    class Meta:
        model = Recipe
        # fields = '__all__'
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            # 'is_favorite',
            # 'is_in_shopping_cart'
            'name',
            # 'image',
            'text',
            'cooking_time',
        )
        read_only_fields = ('author',)

    def create(self, validated_data):
        # validated_data['author'] = self.context['request'].user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredient_recipe')
        recipe = Recipe.objects.create(**validated_data)
        for i in ingredients:
            ingredient = i['id']
            IngredientRecipe.objects.create(
                ingredient=ingredient,
                recipe=recipe,
                amount=i['amount'],
            )
        for tag in tags:
            TagRecipe.objects.create(recipe=recipe, tag=tag)
            return recipe


    #     # Добавляем автора рецепта
    #     return super(RecipeCreateSerializer, self).create(validated_data)


#     def create(self, validated_data):
#         if 'tags' not in self.initial_data:
#             recipe = Recipe.objects.create(**validated_data)
#             return recipe
#         tags = validated_data.pop('tags')
#         recipe = Recipe.objects.create(**validated_data)

#         for tag in tags:
#             current_tag, status = Tag.objects.get_or_create(**tag)
#             TagRecipe.objects.create(tag=current_tag, recipe=recipe)
#         return recipe


class RecipeListSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(
        read_only=True,
    )
    tags = TagSerializer(
        many=True,
        required=False,
    )
    ingredients = IngredientRecipeSerializer(
        source='ingredient_recipe',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Recipe
        fields = '__all__'
