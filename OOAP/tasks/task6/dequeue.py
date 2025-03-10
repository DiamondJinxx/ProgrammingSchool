import abc
from typing import Generic, TypeVar

T = TypeVar("T")

class AbstractQueue(Generic[T], abc.ABC):
    """АТД Двунаправленной FIFO/LIFO очереди"""

    POP_FRONT_OK = 0 # последний вызов pop_front() успешен
    POP_FRONT_ERR = 1 # очередь пуста

    PEEK_OK = 0 # последний вызов pop() успешен
    PEEK_ERR = 1 # очередь пуста

    # конструктор
    # постусловие: создана пустая очередь
    def __init__(self) -> None:
        """Конструктор очереди"""

    # Команды

    # постусловие: элемент добавлен в конец очереди
    @abc.abstractmethod
    def push_back(self, value: T) -> None:
        """Добавить элемент в очередь"""

    # предусловие: очередь не пуста
    # постусловие: первый элемент удаляется из очереди
    @abc.abstractmethod
    def pop_front(self) -> T:
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
    
    # дополнительные запросы
    @abc.abstractmethod
    def get_pop_front_status() -> int:
        """Получить статус выполнения команды pop_front. Возвращает значение POP_FORNT_*"""

    @abc.abstractmethod
    def get_peek_front_status() -> int:
        """Получить статус выполнения команды peek. Возвращает значение PEEK_FORNT_*"""


class Queue(AbstractQueue[T]):
    """АТД однонаправленной FIFO очереди"""


class Dequeue(AbstractQueue[T]):
    """АТД двунправленной FIFO/LIFO очереди"""

    POP_BACK_OK = 0 # последний вызов pop_back() успешен
    POP_BACK_ERR = 1 # очередь пуста

    PEEK_BACK_OK = 0 # последний вызов peek_back() успешен
    PEEK_BACK_ERR = 1 # очередь пуста


    # Команды
    # постусловие: элемент добавляется в начало очереди
    @abc.abstractmethod
    def push_front(self) -> T:
        """Добавить элемент в начало очереди"""

    # предусловие: очередь не пуста
    # постусловие: последний элемент удаляется из очереди
    @abc.abstractmethod
    def pop_back(self) -> T:
        """Забрать элемент с конца очереди"""

    # Запросы
    # предусловие: очередь не пуста
    @abc.abstractmethod
    def peek_back(self):
        """Получить последний элемент в очереди без удаления"""

    # Дополнительные запросы
    @abc.abstractmethod
    def get_pop_back_status() -> int:
        """Получить статус выполнения команды pop_back. Возвращает значение POP_BACK_*"""

    @abc.abstractmethod
    def get_peek_back_status() -> int:
        """Получить статус выполнения команды PEEK_back. Возвращает значение PEEK_BACK*"""
