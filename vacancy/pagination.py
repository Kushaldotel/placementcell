from rest_framework.pagination import PageNumberPagination

class JobVacancyPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Allows frontend to change page size
    max_page_size = 100  # Maximum limit to prevent abuse
