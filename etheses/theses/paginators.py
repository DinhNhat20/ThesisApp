from rest_framework import pagination


class ThesisPaginator(pagination.PageNumberPagination):
    page_size = 5


class Thesis01Paginator(pagination.PageNumberPagination):
    page_size = 5


class CouncilPaginator(pagination.PageNumberPagination):
    page_size = 5


class commonPaginator(pagination.PageNumberPagination):
    page_size = 5
