def is_subscribed(self, data):
    """Retrun TRUE if user has any follower."""
    user = self.context['request'].user
    result = (
        user.is_authenticated
        and data.follower.filter(
            following=user
        ).exists()
    )

    return result
