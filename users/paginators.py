from rest_framework.pagination import PageNumberPagination


class HabitCoursesPaginator(PageNumberPagination):
    """Класс пагинатор для постраничного вывода привычек"""

    page_size = 5
    page_size_query_param = "per-page"
    max_page_size = 100
