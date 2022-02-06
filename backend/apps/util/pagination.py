from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Настройка количества объектов на странице.
    """

    # Количество объектов на странице.
    page_size = 50
    # Наименование параметра для контроля page_size
    page_size_query_param = 'page_size'

