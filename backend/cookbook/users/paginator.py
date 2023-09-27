from rest_framework.pagination import PageNumberPagination


class FollowCustomPaginator(PageNumberPagination):
    """Custom paginator for Follow model."""
    page_size_query_param = 'limit'
    page_query_param = 'page'
