from drf_extra_fields.fields import Base64ImageField
from djoser.serializers import UserSerializer
from rest_framework import serializers, exceptions, status


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


# class UserSerializer(UserSerializer):
class UserSerializer(serializers.ModelSerializer):
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


class FollowSerializer(UserSerializer):
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = UserSerializer.Meta.fields + ('recipes_count', 'recipes')
        read_only_fields = ('email', 'username')

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if Follow.objects.filter(author=author, user=user).exists():
            raise exceptions.ValidationError(
                detail='Вы уже подписаны на этого пользователя!',
                code=status.HTTP_400_BAD_REQUEST,
            )
        if user == author:
            raise exceptions.ValidationError(
                detail='Вы не можете подписаться на самого себя!',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[: int(limit)]
        return RecipeShortSerializer(
            recipes,
            many=True,
            read_only=True,
        ).data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='ingredient.id',
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name',
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
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
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeCreateSerializer(
        source='ingredientrecipes',
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
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
    
    def create_ingredients(self, ingredients, recipe):
        for ing in ingredients:
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient=ing['id'],
                amount=ing['amount'],
            )

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredientrecipes')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients(ingredients, recipe)
        # for i in ingredients:
        #     IngredientRecipe.objects.create(
        #         recipe=recipe,
        #         ingredient=i['id'],
        #         amount=i['amount'],
        #     )
        recipe.tags.set(tags)
        # for tag in tags:
        #     TagRecipe.objects.create(recipe=recipe, tag=tag)
        return recipe

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context=self.context).data

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredientrecipes')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients(ingredients, instance)
        # for i in ingredients:
        #     IngredientRecipe.objects.create(
        #         recipe=instance,
        #         ingredient=i['id'],
        #         amount=i['amount'],
        #     )
        instance.save()
        return instance


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(
        read_only=True,
    )
    tags = TagSerializer(
        many=True,
        read_only=True,
    )
    ingredients = IngredientRecipeSerializer(
        source='ingredientrecipes',
        many=True,
        read_only=True,
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and user.favorites.filter(recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and user.shoppingcarts.filter(recipe=obj).exists()
        )


class RecipeShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = (
            'user',
            'recipe',
        )

    def validate(self, data):
        if Favorite.objects.filter(
            user_id=data['user'], recipe_id=data['recipe']
        ):
            raise serializers.ValidationError(
                {'favorite': 'Рецепт уже в вашем избранном'}
            )
        return data

    # def create(self, validated_data):
    #     recipe = validated_data['recipe']
    #     Favorite.objects.create(user=validated_data['user'], recipe=recipe)
    #     return recipe

    def to_representation(self, instance):
        return RecipeShortSerializer(instance).data


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = (
            'user',
            'recipe',
        )

    def validate(self, data):
        if ShoppingCart.objects.filter(
            user_id=data['user'], recipe_id=data['recipe']
        ):
            raise serializers.ValidationError(
                {'shoppingcarts': 'Рецепт уже в вашей корзине'}
            )
        return data

    # def create(self, validated_data):
    #     recipe = validated_data['recipe']
    #     ShoppingCart.objects.create(user=validated_data['user'], recipe=recipe)
    #     return recipe

    def to_representation(self, instance):
        return RecipeShortSerializer(instance).data
