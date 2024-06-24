from rest_framework import pagination


class ThesisPaginator(pagination.PageNumberPagination):
    page_size = 3


class Thesis01Paginator(pagination.PageNumberPagination):
    page_size = 5


class CouncilPaginator(pagination.PageNumberPagination):
    page_size = 4


class commonPaginator(pagination.PageNumberPagination):
    page_size = 5
