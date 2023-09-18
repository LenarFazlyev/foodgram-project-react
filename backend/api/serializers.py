from rest_framework import serializers
from djoser.serializers import UserSerializer


from recipes.models import (
    Recipe,
    Tag,
    TagRecipe,
    Ingredient,
    IngredientRecipe,
)
from users.models import (User, Follow)


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
            'is_subscribed'
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


# class RecipeSerializer(serializers.ModelSerializer):
#     # author = serializers.SlugRelatedField(
#     #     # read_only=True,
#     #     slug_field='first_name',
#     # )
#     tags = TagSerializer(many=True, required=False)
#     ingredients = IngredientrecipeSerializer(
#         source='ingredient',
#         many=True,
#         read_only=True,
#     )

#     class Meta:
#         model = Recipe
#         fields = '__all__'
#         # fields = ('id', 'author', 'name', 'text', 'ingredients', 'tags')

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
    ingredients = IngredientrecipeSerializer(
        source='ingredient',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Recipe
        fields = '__all__'
