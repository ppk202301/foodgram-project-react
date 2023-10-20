from rest_framework.pagination import PageNumberPagination


class UsersCustomPaginator(PageNumberPagination):
    """Custom paginator for Users Application."""
    page_size_query_param = 'limit'
    page_query_param = 'page'


class FollowCustomPaginator(UsersCustomPaginator):
    """Custom paginator for Follow model."""
    pass


class UserCustomPaginator(UsersCustomPaginator):
    """Custom paginator for User model."""
    pass
