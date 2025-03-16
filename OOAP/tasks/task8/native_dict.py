import abc
from typing import Generic, TypeVar

V = TypeVar("V")

class AbstractNativeDict(Generic[V], abc.ABC):
    """АТД ассоциативного массива."""

    PUT_OK = 0 # последний вызов put() успешен
    PUT_ERR = 1 # ключ уже существует

    GET_OK = 0 # последний вызов get() успешен
    GET_ERR = 1 # ключ отсутствует в словаре

    REMOVE_OK = 0 # последний вызов remove() успешен
    REMOVE_ERR = 1 # ключ отсутствует в словаре

    # конструктор
    # постусловие: создан пустой словарь заданного размера
    def __init__(self, size: int) -> None:
        """Конструктор словаря"""

    # Команды

    # предусловие: в словаре отсутствует элемент по заданному ключу
    # постусловие: элемент добавлен в словарь
    @abc.abstractmethod
    def put(self, key: str, value: V) -> None:
        """Добавить элемент в словарь по ключу"""

    # предусловие: в словаре присутствует элемент по заданному ключу
    @abc.abstractmethod
    def get(self, key: str) -> V:
        """Запрос элемента по ключу"""

    # предусловие: в словаре присутствует элемент по переданному ключу
    # постусловие: элемент по переданному ключу удален из словаря
    @abc.abstractmethod
    def remove(self, key: K) -> None:
        """Удалить элемент из словаря по ключу"""

    # Запросы
    @abc.abstractmethod
    def contains(self, key: str) -> bool:
        """Запрос проверки наличия ключа в словаре"""

    @abc.abstractmethod
    def size(self) -> int:
        """Запрос размере словаря"""

    # Дополнительные запросы

    @abc.abstractmethod
    def get_put_status() -> int:
        """Получить статус выполнения команды put. Возвращает значение PUT_*"""

    @abc.abstractmethod
    def get_get_status() -> int:
        """Получить статус выполнения команды get. Возвращает значение GET_*"""

    @abc.abstractmethod
    def get_remove_status() -> int:
        """Получить статус выполнения команды remove. Возвращает значение REMOVE_*"""
