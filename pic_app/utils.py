"""Вспомогательный файл для утилит."""

from django.core.paginator import Paginator, Page
from django.core.cache import caches
from django.http import HttpRequest

DatabaseCache = caches["database"]
cache = caches["default"]
ram_cache = caches["ram_cache"]


class CustomCache:
    """Кеширование данных."""

    @staticmethod
    def caching(key: str, lambda_func: callable, timeout: int = 1) -> any:
        """Попытка взять или записать кэш."""

        data = cache.get(key)
        if data is None:
            data = lambda_func()
            cache.set(key, data, timeout=timeout)
        return data

    @staticmethod
    def clear_cache(key: str) -> any:
        """Очистка кэша."""

        cache.set(key, None, timeout=1)

    @staticmethod
    def set_cache(key: str, data: any, timeout: int = 1):
        """."""

        cache.set(key, data, timeout=timeout)


class CustomPaginator:
    """Постраничный вывод данных."""

    @staticmethod
    def paginate(object_list: any, request: HttpRequest, limit: int = 15) -> Page:
        """Пагинация данных."""

        _paginator = Paginator(object_list, limit)
        _page = _paginator.get_page(request.GET.get(key="page", default=1))  # http://127.0.0.1:8000/ratings/top/?page=1  # path parameter
        return _page

    @staticmethod
    def get_page_array(num: int, max_page: int) -> list:
        """Возвращает ограниченный массив страниц."""

        if num <= 3:
            return [1, 2, 3]
        if num >= max_page - 2:
            return [max_page - 2, max_page - 1, max_page]
        return [x for x in range(num - 2, num + 3)]