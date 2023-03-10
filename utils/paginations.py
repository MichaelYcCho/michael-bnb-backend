from rest_framework.pagination import PageNumberPagination


class RoomReviewPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    ordering = "-id"


class RoomAmenitiesPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = "page_size"
    ordering = "-id"
