from django.contrib import admin

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'first_name', 'last_name'
    )
    list_filter = ('username', 'email',)
    list_display_links = ('username', 'email',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'user')
    list_display_links = ('author', 'user',)


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
