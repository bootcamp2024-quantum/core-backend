from rest_framework import generics, pagination


class RoadmapSearchPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10
