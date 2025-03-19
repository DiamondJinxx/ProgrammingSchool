import abc
from typing import Generic, TypeVar

T = TypeVar("T")

class AbstractHashmap(Generic[T], abc.ABC):
    """АТД Хеш-таблицы"""

    PUT_OK = 0 # последний вызов put() успешен
    PUT_ERR = 1 # ошибка при добавлении элемента в очередь.

    REMOVE_OK = 0 # последний вызов remove() успешен
    REMOVE_ERR = 1 # значение отсутствует в таблице

    # конструктор
    # постусловие: создана пустая хеш-таблица с заданным максимальным размером
    def __init__(self, max_size: int) -> None:
        """Конструктор хеш-таблицы"""

    # Команды

    # предусловие: в таблице есть место под значение
    # постусловие: элемент добавлен таблицу
    @abc.abstractmethod
    def put(self, value: T) -> None:
        """Добавить элемент в таблицу"""

    # предусловие: в таблице присутствует элемент по переданному ключу
    # постусловие: элемент по переданному ключу удален из таблицы
    @abc.abstractmethod
    def remove(self, value: T) -> None:
        """Удалить элемент из таблицы по ключу"""

    # Запросы
    @abc.abstractmethod
    def contains(self, value: T) -> bool:
        """Запрос проверки наличия элемента в таблице"""

    # Дополнительные запросы

    @abc.abstractmethod
    def get_put_status() -> int:
        """Получить статус выполнения команды put. Возвращает значение PUT_*"""

    @abc.abstractmethod
    def get_remove_status() -> int:
        """Получить статус выполнения команды remove. Возвращает значение REMOVE_*"""


class AbstractPowerSet(AbstractHashmap[T]):
    """АТД множества"""

    # Запросы
    @abc.abstractmethod
    def intersection(self, other_set: Self) -> Self:
        """Запрос пересечения с другим множеством"""

    @abc.abstractmethod
    def union(self, other_set: Self) -> Self:
        """Запрос объединения с другим множеством"""

    @abc.abstractmethod
    def diff(self, other_set: Self) -> Self:
        """Запрос разницы с другим множеством"""

    @abc.abstractmethod
    def is_subset(self, other_set: Self) -> bool:
        """Проверить является ли множество подмножеством передаваемого множества"""

    @abc.abstractmethod
    def is_equals(self, other_set: Self) -> bool:
        """Проверить равенство двух множеств"""
