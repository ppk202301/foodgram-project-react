from rest_framework.pagination import PageNumberPagination


class Paginator(PageNumberPagination):
    """Custom pagination class."""
    page_query_param = 'page'
