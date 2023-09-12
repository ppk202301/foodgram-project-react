from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom model User."""
    REQUIRED_FIELDS = ('first_name', 'last_name', 'email')

    email = models.EmailField(
        'Email',
        max_length=254,
        unique=True
    )

    bio = models.TextField(
        'About',
        max_length=300,
        blank=True
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Follow to author of recipe model."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Follower'
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Author'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='user_following'
            ),
            models.CheckConstraint(
                check=~models.Q(following=models.F('user')),
                name='protect_self_following'
            ),
        ]

    def __str__(self):
        return f'Author {self.following} has follower {self.user}.'
