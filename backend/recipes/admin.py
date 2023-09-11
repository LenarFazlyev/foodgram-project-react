from django.contrib import admin

from .models import Tag, Recipe, Ingredient
# from .models import Recipe, Author, Tag, TagRecipe

class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_editable = ('author',)
    search_fields = ('author', 'name', 'tags')
    list_filter = ('author', 'name', 'tags')

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)




admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)

