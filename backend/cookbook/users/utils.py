def is_subscribed(self, data):
    """Retrun TRUE if user has any follower."""
    user = self.context['request'].user
    return (
        user.is_authenticated and
        data.follower.filter(
            following = user
        ).exists()
    )
