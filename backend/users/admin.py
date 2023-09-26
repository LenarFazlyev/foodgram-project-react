from django.contrib import admin

from users.models import User, Follow


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'password',
    )
    fields = (
        'email',
        'username',
        'first_name',
        'last_name',
        'password',
    )
    list_filter = (
        'email',
        'first_name',
    )
    list_editable = (
        'username',
        'first_name',
        'last_name',
    )


class FollowAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
