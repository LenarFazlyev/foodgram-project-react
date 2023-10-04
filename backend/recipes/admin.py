from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from .models import (
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


class TagInLine(admin.TabularInline):
    model = Recipe.tags.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'display_ingredients',
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

    def display_ingredients(self, obj):
        return mark_safe(
            ', '.join(
                [ingredient.name for ingredient in obj.ingredients.all()]
            )
        )

    display_ingredients.short_description = 'Ингридиенты'

    def favorite_count(self, obj):
        return obj.favorites.count()

    favorite_count.short_description = 'Кол-во в Избранном'

    def display_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" height="60">')

    display_image.short_description = 'Изображение'


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
)  # Здесь не сразу догадался использовать unregister
