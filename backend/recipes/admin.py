from django.contrib import admin

from .models import (
    Tag,
    TagRecipe,
    Recipe,
    Ingredient,
    IngredientRecipe,
)



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')


@admin.register(TagRecipe)
class TagRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tag', 'recipe')
    list_editable = ('tag', 'recipe')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
    )
    list_editable = ('author',)
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


# admin.site.register(Recipe, RecipeAdmin)
# admin.site.register(Tag, TagAdmin)
# admin.site.register(TagRecipe, TagRecipeAdmin)
# admin.site.register(Ingredient, IngredientAdmin)
# admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
