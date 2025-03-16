import abc
from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")

class AbstractHashmap(Generic[K,V], abc.ABC):
    """АТД Хеш-таблицы"""

    PUT_OK = 0 # последний вызов put() успешен
    PUT_ERR = 1 # ошибка при добавлении элемента в очередь.

    REMOVE_OK = 0 # последний вызов remove() успешен
    REMOVE_ERR = 1 # значение отсутствует в таблице

    # конструктор
    # постусловие: создана пустая хеш-таблица
    def __init__(self) -> None:
        """Конструктор хеш-таблицы"""

    # Команды

    # предусловие: в таблице отсутствует элемент по заданному ключу
    # постусловие: элемент добавлен таблицу
    @abc.abstractmethod
    def put(self, key: K, value: V) -> None:
        """Добавить элемент в таблицу"""

    # предусловие: в таблице присутствует элемент по переданному ключу
    # постусловие: элемент по переданному ключу удален из таблицы
    @abc.abstractmethod
    def remove(self, key: K) -> None:
        """Удалить элемент из таблицы по ключу"""

    # Запросы
    @abc.abstractmethod
    def contains(self, value: V) -> bool:
        """Запрос проверки наличия элемента в таблице"""

    # Дополнительные запросы

    @abc.abstractmethod
    def get_put_status() -> int:
        """Получить статус выполнения команды put. Возвращает значение PUT_*"""

    @abc.abstractmethod
    def get_remove_status() -> int:
        """Получить статус выполнения команды remove. Возвращает значение REMOVE_*"""
