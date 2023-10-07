from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from foodgram import constants
from recipes.models import (
    Tag,
    TagRecipe,
    Recipe,
    Ingredient,
    IngredientRecipe,
    Favorite,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')


@admin.register(TagRecipe)
class TagRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tag', 'recipe')
    list_editable = ('tag', 'recipe')


class IngredientInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    min_num = constants.MAXQUANTITY


class TagInLine(admin.TabularInline):
    model = Recipe.tags.through
    min_num = constants.MAXQUANTITY


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'display_ingredients',
        'display_tags',
        'favorite_count',
        'display_image',
    )
    list_display_links = (
        'name',
        'author',
        'display_ingredients',
    )
    search_fields = (
        'author',
        'name',
        'tags',
    )
    list_filter = (
        'author',
        'name',
        'tags',
    )
    inlines = (
        IngredientInLine,
        TagInLine,
    )

    @admin.display(description='Ингедиенты')
    def display_ingredients(self, obj):
        return mark_safe(
            ', '.join(
                [ingredient.name for ingredient in obj.ingredients.all()]
            )
        )

    @admin.display(description='Тэги')
    def display_tags(self, obj):
        return mark_safe(
            ', '.join(
                [tag.name for tag in obj.tags.all()]
            )
        )

    @admin.display(description='Кол-во в Избранном')
    def favorite_count(self, obj):
        return obj.favorites.count()

    @admin.display(description='Изображение')
    def display_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" height="60">')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(
    Group
)
