from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Follow,
    User
)


@admin.register(User)
class UserAdmin(UserAdmin):
    """Admin panel of User model."""
    list_display = (
        'id',
        'is_active',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio'
    )
    list_filter = (
        'username',
        'email'
    )
    search_fields = (
        'username',
        'email'
    )
    list_editable = (
        'is_active',
    )

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Admin panel of Follow model."""
    list_display = ('id', 'user', 'following',)
