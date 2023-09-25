from drf_extra_fields.fields import Base64ImageField
from djoser.serializers import UserSerializer
from rest_framework import serializers


from recipes.models import (
    Recipe,
    Tag,
    TagRecipe,
    Ingredient,
    IngredientRecipe,
    Favorite,
    ShoppingCart,
)
from users.models import User, Follow


class CustomUserSerializer(UserSerializer):
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
    

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'amount',
        )



class RecipeCreateSerializer(serializers.ModelSerializer):
    # author = serializers.PrimaryKeyRelatedField(read_only=True)
    ingredients = IngredientRecipeCreateSerializer(
        source='ingredientrecipes',
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    image = Base64ImageField()


    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = ('author',)


    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = []
        for i in ingredients:
            amount = i['amount']
            if int(amount) < 1:
                raise serializers.ValidationError(
                    {'amount': 'Количество ингредиента должно быть больше 0!'}
                )
            if i['id'] in ingredients_list:
                raise serializers.ValidationError(
                    {'ingredient': 'Ингредиенты должны быть уникальными!'}
                )
            ingredients_list.append(i['id'])
        return data


    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredientrecipes')
        recipe = Recipe.objects.create(**validated_data)
        for i in ingredients:
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient=i['id'],
                amount=i['amount'],
            )
        for tag in tags:
            TagRecipe.objects.create(recipe=recipe, tag=tag)
        return recipe
    
    def to_representation(self, instance):
        serializer = RecipeReadSerializer(instance, context=self.context)
        return serializer.data


class RecipeReadSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(
        read_only=True,
    )
    tags = TagSerializer(
        many=True,
        required=False,
    )
    ingredients = IngredientRecipeSerializer(
        source='ingredientrecipes',
        many=True,
        read_only=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    # image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        # fields = '__all__'
        exclude = ('pub_date',)
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe_id=obj).exists()
    
    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=request.user, recipe_id=obj).exists()
    
    # def get_image(self, obj):
    #     if obj.image:
    #         return obj.image.url
    #     return
