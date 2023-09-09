from django.contrib import admin

from .models import Tag, Recipe
# from .models import Recipe, Author, Tag, TagRecipe

class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    # list_editable = ('name',)
    search_fields = ('author', 'name', 'tags')
    list_filter = ('author', 'name', 'tags')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
