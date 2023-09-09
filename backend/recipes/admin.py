from django.contrib import admin

from .models import Tag

class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')

# from .models import Recipe, Author, Tag, TagRecipe


# class RecipeAdmin(admin.ModelAdmin):
#     list_display = (
#         'pk',
#         'title',
#         'author',
#         'pub_date',
#         'description',
#     )
#     # list_editable =
#     search_fields = ('description',)
#     list_filter = (
#         'pub_date',
#         'cookingtime',
#     )
#     empty_value = '-пусто-'


# admin.site.register(
#     Recipe,
#     RecipeAdmin,
# )
# admin.site.register(Author)
admin.site.register(Tag, TagAdmin)
# admin.site.register(TagRecipe)
