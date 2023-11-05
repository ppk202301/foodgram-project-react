def is_subscribed(self, data):
    """Retrun TRUE if User has follower pointed in data."""
    user = self.context['request'].user

    return (
        user.is_authenticated
        and user.follower.filter(
            following=data
        ).exists()
    )
