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
        'is_staff',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio'
    )
    list_editable = (
        'is_active',
        'is_staff',
    )
    list_filter = (
        'username',
        'email'
    )
    search_fields = (
        'username',
        'email'
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Admin panel of Follow model."""
    list_display = (
        'user',
        'following',
    )
    list_filter = (
        'user',
        'following',
    )
    search_fields = (
        'user',
        'following',
    )
