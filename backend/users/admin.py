from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as ModelUserAdmin

from users.models import User, Follow


@admin.register(User)
class UserAdmin(ModelUserAdmin):
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

    @admin.display(description='Количество рецептов')
    def get_recipe_count(self, obj):
        return obj.recipes.count()

    @admin.display(description='Количество подписчиков')
    def get_follower_count(self, obj):
        return obj.follower.count()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass
