from drf_extra_fields.fields import Base64ImageField
from django.core.validators import MinValueValidator, MaxValueValidator
from djoser.serializers import UserSerializer
from rest_framework import serializers, exceptions, status


from recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    IngredientRecipe,
    Favorite,
    ShoppingCart,
)
from foodgram import constants
from users.models import User, Follow


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
        return request.user.is_authenticated and bool(
            request.user.follower.filter(author=obj)
        )


class FollowPostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('user', 'author')

    def validate(self, data):
        if Follow.objects.filter(
            author=data['author'].id, user=data['user'].id
        ).exists():
            raise exceptions.ValidationError(
                detail='Вы уже подписаны на этого пользователя!',
                code=status.HTTP_400_BAD_REQUEST,
            )
        if data['author'].id == data['user'].id:
            raise exceptions.ValidationError(
                detail='Вы не можете подписаться на самого себя!',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data

    def to_representation(self, instance):
        return FollowSerializer(
            instance.author, context={'request': self.context['request']}
        ).data


class FollowSerializer(UserSerializer):
    recipes_count = serializers.ReadOnlyField(source='recipes.count')
    recipes = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = UserSerializer.Meta.fields + ('recipes_count', 'recipes')
        read_only_fields = ('email', 'username')

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            try:
                recipes = recipes[: int(limit)]
            except:
                raise exceptions.ValidationError(
                    'Параметр лимит должен быть цифрой'
                )
        serializer = RecipeShortSerializer(recipes, many=True, read_only=True)
        return serializer.data


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
    amount = serializers.IntegerField(
        validators=[
            MinValueValidator(
                constants.MINQUANTITY,
                message='Минимальное количество должно быть больше 0 г',
            ),
            MaxValueValidator(
                constants.MAXQUANTITY,
                message=f'Максимальный вес не больше {constants.MAXQUANTITY} г',
            ),
        ]
    )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'amount',
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeCreateSerializer(
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    image = Base64ImageField()

    cooking_time = serializers.IntegerField(
        validators=[
            MinValueValidator(
                constants.MINTIME,
                message='Время приготовления должно быть больше 0',
            ),
            MaxValueValidator(
                constants.MAXTIME,
                message=(
                    f'Время приготовления не может превышать {constants.MAXTIME} минут'
                ),
            ),
        ]
    )

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
        tags = self.initial_data.get('tags')
        if not tags:
            raise serializers.ValidationError(
                {'tags': 'ВЫберите хотябы один тэг'}
            )
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError(
                {'tags': 'Нельзя добавлять одинаковые тэги'}
            )
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                {'amount': 'Нельзя создат рецепт без ингредиентов'}
            )

        if len(ingredients) != len(set([x['id'] for x in ingredients])):
            raise serializers.ValidationError(
                {'ingredient': 'Ингредиенты должны быть уникальными!'}
            )
        if not self.initial_data.get('image'):
            raise serializers.ValidationError(
                {'image': 'Без картинки не создается рецепт'}
            )

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
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return recipe

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context=self.context).data

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients(ingredients, instance)
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
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField()

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
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = Favorite
        fields = (
            'user',
            'recipe',
        )

    def validate(self, data):
        if Favorite.objects.filter(user=data['user'], recipe=data['recipe']):
            raise serializers.ValidationError(
                {'favorite': 'Рецепт уже в вашем избранном'}
            )
        return data

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe, context={'request': self.context.get('request')}
        ).data


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

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe, context={'request': self.context.get('request')}
        ).data