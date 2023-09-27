def is_subscribed(self, data):
    user = self.context['request'].user
    return (
        user.is_authenticated and
        data.follower.filter(
            following = user
        ).exists()
    )
