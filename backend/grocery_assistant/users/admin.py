from django.contrib import admin

from .models import Follow, User


class UsserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'first_name', 'last_name'
    )
    list_filter = ('username', 'email',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'user')


admin.site.register(User, UsserAdmin)
admin.site.register(Follow, FollowAdmin)
