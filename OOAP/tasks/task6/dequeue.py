import abc
from typing import Generic, TypeVar

T = TypeVar("T")

class AbstractDequeue(Generic[T], abc.ABC):
    """АТД Двунаправленной FIFO/LIFO очереди"""

    POP_OK = 0 # последний вызов pop() успешен
    POP_ERR = 1 # очередь пуста

    PEEK_OK = 0 # последний вызов pop() успешен
    PEEK_ERR = 1 # очередь пуста

    # конструктор
    # постусловие: создана пустая очередь
    def __init__(self) -> None:
        """Конструктор очереди"""

    # Команды

    # постусловие: элемент добавлен в очередь
    @abc.abstractmethod
    def push(self, value: T) -> None:
        """Добавить элемент в очередь"""

    # предусловие: очередь не пуста
    # постусловие: первый элемент удаляется из очереди
    @abc.abstractmethod
    def pop(self) -> T:
        """Забрать элемент с начала очереди"""


    # постусловие: очередь отчищена
    @abc.abstractmethod
    def clear(self) -> None:
        """Отчистить очередь"""

    # Запросы

    # предусловие: очередь не пуста
    @abc.abstractmethod
    def peek(self) -> int:
        """Запрос первого элемента очереди без удаления"""


    @abc.abstractmethod
    def size(self) -> int:
        """Запрос размера очереди"""

    @abc.abstractmethod
    def contains(self, value: T) -> bool:
        """Содержит ли очередь элемент с переданным значением"""

    # дополнительные запросы
    @abc.abstractmethod
    def get_pop_status() -> int:
        """Получить статус выполнения команды pop. Возвращает значение POP_*"""

    @abc.abstractmethod
    def get_peek_status() -> int:
        """Получить статус выполнения команды peek. Возвращает значение PEEK_*"""
