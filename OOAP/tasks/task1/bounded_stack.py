import abc
from typing import  TypeVar, List, Generic

T = TypeVar("T")

class AbstractBoundedStack(Generic[T], abc.ABC):

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

    #предусловие: стек не пустой
    #постусловие: из стека удален верхний элемент
    @abc.abstractmethod
    def pop(self) -> None:
        """Удалить из стека верхний элемент"""

    #предусловие: стек не пустой
    @abc.abstractmethod
    def peek(self) -> T:
        """Получить верхний элемент стека"""

    @abc.abstractmethod
    def size(self) -> int:
        """Получить размер стека"""

    #постусловие: из стека удаляются все значения
    @abc.abstractmethod
    def clear(self) -> None:
        """Отчистить стек"""

    # дополнительные методы
    @abc.abstractmethod
    def get_peek_status(self) -> int:
        """Получить стастус выполнения запроса peek"""

    @abc.abstractmethod
    def get_pop_status(self) -> int:
        """Получить стастус выполнения команды pop"""

    @abc.abstractmethod
    def get_push_status(self) -> int:
        """Получить стастус выполнения команды push"""


class BoundedStack(AbstractBoundedStack[T]):
    __stack: List[T] # основное хранилище
    __size_limit: int # максимальное число элементов стека
    __peek_status: int # статус запроса peek
    __pop_status: int # статус команды pop
    __push_status: int # статус команды push

    # конструктор
    # постусловие: создан пустой стэк с заданым ограничением максимального числа элементов
    def __init__(self, max_size: int = 32) -> None:
        self.__size_limit = max_size
        self.__stack = []

    def push(self, value: T) -> None:
        if self.size() < self.__size_limit:
            self.__stack.append(value)
            self.__push_status = self.PUSH_OK
            return
        self.__push_status = self.PUSH_ERR

    def pop(self) -> None:
        if self.size() > 0:
            self.__stack.pop()
            self.__pop_status = self.POP_OK
            return
        self.__pop_status = self.POP_ERR

    def peek(self) -> T:
        result = 0
        self.__peek_status = self.PEEK_ERR
        if self.size() > 0:
            result = self.__stack[-1]
            self.__peek_status = self.PEEK_OK
        return result

    def size(self) -> int:
        return len(self.__stack)

    def clear(self) -> None:
        self.__stack = []
        self.__pop_status = self.POP_NIL
        self.__peek_status = self.PEEK_NIL

    def get_peek_status(self) -> int:
        return self.__peek_status

    def get_pop_status(self) -> int:
        return self.__pop_status

    def get_push_status(self) -> int:
        return self.__push_status

