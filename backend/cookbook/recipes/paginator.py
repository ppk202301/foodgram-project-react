from rest_framework.pagination import PageNumberPagination


class RecipeCustomPaginator(PageNumberPagination):
    """Custom paginator for Users Application."""
    page_size_query_param = 'limit'
    page_query_param = 'page'
