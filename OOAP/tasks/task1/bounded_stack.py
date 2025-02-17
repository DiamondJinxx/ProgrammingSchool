import abc
from typing import  TypeVar, List, Generic

T = TypeVar("T")

class AbstractBoundedStack(Generic[T], abc.ABC):
    __stack: List[T] # основное хранилище
    __peek_status: int # статус запроса peek
    __pop_status: int # статус команды pop
    __push_status: int # статус команды push

    #предусловие: текущий размер стека строго меньше максимально допустимого размера
    #постусловие: в стэк добавлено новое значение
    @abc.abstractmethod
    def push(value: T) -> None:
        """Добавить значение в стек"""

    #предусловие:
    #постусловие:
    @abc.abstractmethod
    def pop() -> T:
        """"""

    #предусловие:
    #постусловие:
    @abc.abstractmethod
    def peek() -> T:
        """"""

    #предусловие:
    #постусловие:
    @abc.abstractmethod
    def size() -> T:
        """"""

    #предусловие:
    #постусловие:
    @abc.abstractmethod
    def clear() -> T:
        """"""
