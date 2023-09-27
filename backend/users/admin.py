from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, Follow


@admin.register(User)
class CustomedUserAdmin(UserAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'get_recipe_count',
        'get_follower_count',
    )
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name', 'last_name')}),
    )
    list_filter = (
        'email',
        'first_name',
    )

    def get_recipe_count(self, obj):
        return obj.recipes.count()
    get_recipe_count.short_description = 'Количество рецептов'

    def get_follower_count(self, obj):
        return obj.follower.count()
    get_follower_count.short_description = 'Количество подписчиков'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass
