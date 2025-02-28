from django.conf import settings

from rest_framework.settings import api_settings
from rest_framework.pagination import PageNumberPagination as CorePageNumberPagination


__all__ = ('PageNumberPagination',)


class PageNumberPagination(CorePageNumberPagination):
    page_size = api_settings.PAGE_SIZE
    max_page_size = settings.REST_FRAMEWORK.get('MAXIMUM_PAGE_SIZE', 100)
    page_size_query_param = 'size'
