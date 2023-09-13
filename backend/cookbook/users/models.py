from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom model User."""
    REQUIRED_FIELDS = ('first_name', 'last_name', 'email')

    email = models.EmailField(
        'Email',
        max_length=254,
        unique=True,
        help_text='Could not be empty.'
    )

    bio = models.TextField(
        'About',
        max_length=300,
        blank=True,
        help_text='Write some words about yourself.'
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'{self.username}'


class Follow(models.Model):
    """Follow to the author of the recipe model."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Follower',
        help_text='Point the user interested in the author.'
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Author',
        help_text='Any interesting author.'
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(following=models.F('user')),
                name='protect_self_following'
            ),
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='user_following'
            ),
        ]

    def __str__(self):
        return (
            f'Author {self.following.username} '
            f'has follower {self.user.username}'
        )
