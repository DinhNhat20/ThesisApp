from rest_framework import pagination


class ThesisPaginator(pagination.PageNumberPagination):
    page_size = 5


class commonPaginator(pagination.PageNumberPagination):
    page_size = 5
