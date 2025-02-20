import abc
from typing import Generic, TypeVar

T = TypeVar("T")

class AbstractLinkedList(Generic[T], abc.ABC):
    """АТД связного списка."""

    POP_NIL = 0 # push() ещё не вызывалась
    POP_OK = 1 # последняя pop() отработала нормально
    POP_ERR = 2 # стек пуст

    PEEK_NIL = 0 # push() ещё не вызывалась
    PEEK_OK = 1 # последняя peek() вернула корректное значение 
    PEEK_ERR = 2 # стек пуст

    PUSH_OK = 0 # последний push() отработал корректно
    PUSH_ERR = 1 # стэк полон

    #предусловие: текущий размер стека строго меньше максимально допустимого размера
    #постусловие: в стэк добавлено новое значение
    @abc.abstractmethod
    def push(self,value: T) -> None:
        """Добавить значение в стек"""

