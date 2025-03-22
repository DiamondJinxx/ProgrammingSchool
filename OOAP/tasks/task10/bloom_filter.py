import abc
from typing import Generic, TypeVar

T = TypeVar("T")

class AbstractBloomFilter(Generic[T], abc.ABC):
    """АТД Фильтра Блюма"""

    # конструктор
    # постусловие: создана пустой фильтр Блюма с заданным размером
    def __init__(self, size: int) -> None:
        """Конструктр фильтра"""

    # Команды
    
    # постусловие: элемент добавлен в фильтр
    @abc.abstractmethod
    def add(self, value: T) -> None:
        """Добавить элемент"""

    # Запросы
    @abc.abstractmethod
    def is_value(self, value: T) -> bool:
        """Проверить наличие элемента в фильтре"""

