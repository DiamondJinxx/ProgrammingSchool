import abc
from typing import Generic, TypeVar

T = TypeVar("T")

class AbstractLinkedList(Generic[T], abc.ABC):
    """АТД связного списка."""

    HEAD_NIL = 0 # add_to_empty() ещё не вызывалась
    HEAD_OK = 1 # последняя head() отработала нормально
    HEAD_ERR = 2 # список пуст

    TAIL_NIL = 0 # add_to_empty() ещё не вызывалась
    TAIL_OK = 1 # последняя tail() отработала нормально
    TAIL_ERR = 2 # список пуст

    RIGHT_TAIL = 0 # курсор уже является последним узлом списка
    RIGHT_OK = 1 # последняя right() отработала нормально
    RIGHT_ERR = 2 # список пуст

    PUT_RIGHT_OK = 1 # последний вызов put_right() отработал нормально
    PUT_RIGHT_ERR = 2 # список пуст

    PUT_LEFT_OK = 1 # последний вызов put_left() отработал нормально
    PUT_LEFT_ERR = 2 # список пуст

    REMOVE_RIGHT = 0 # последний вызов remove() отработал нормально и курсор переместился на узел справа
    REMOVE_LEFT = 1 # последний вызов remove() отработал нормально и курсор переместился на узел слева
    REMOVE_ERR = 2 # список пуст

    ADD_TO_EMPTY_OK = 0 # последний вызок add_to_empty() отработал нормально
    ADD_TO_EMPTY_ERR = 1 # список не пуст

    REPLACE_OK = 0 # последний вызок replace() отработал нормально
    REPLACE_ERR = 1 # список пуст
    
    FIND_OK = 0 # последний вызок find() отработал нормально
    FIND_NOT_VALUE = 1 # последний вызок find() отработал нормально, но не было найдено искомое значение
    FIND_ERR = 2 # список пуст

    REMOVE_ALL_OK = 0 # последний вызок remove_all() отработал нормально
    REMOVE_ALL_ERR = 1 # список пуст
    
    # команды

    # предусловие: список не пуст
    # постусловие: курсор установлен на первый узел в списке
    @abc.abstractmethod
    def head(self):
        """Установить курсор на первый узел в списке"""

    # предусловие: список не пуст
    # постусловие: курсор установлен на последний узел в списке
    @abc.abstractmethod
    def tail(self):
        """Установить курсор на последний узел в списке"""
    
    # предусловие: список не пуст, текущий элемент не является последним узлом списка
    # постусловие: курсор сдвинут на один узел вправо, если курсор не является последним узлом списка
    @abc.abstractmethod
    def right(self):
        """Сдвинуть курсор на один узел вправо"""
    
    # предусловие: список не пуст
    # постусловие: следом за текущем узлом добавлен узел с заданным значением
    @abc.abstractmethod
    def put_right(self, value: T):
        """Вставить следом за текущим узлом новый узел с заданным значением"""

    # предусловие: список не пуст
    # постусловие: перед текущем узлом добавлен узел с заданным значением
    @abc.abstractmethod
    def put_left(self, value: T):
        """Вставить следом за текущим узлом новый узел с заданным значением"""
    
    # предусловие: список не пуст
    # постусловие: удален текущий узел, курсор сместился к существующему соседу.
    @abc.abstractmethod
    def remove(self):
        """Удалить текущий узел. Курсор смещается к правому соседу, если он есть, либо к левому, если он есть."""
    
    # постусловие: из списка удаляются все узлы
    @abc.abstractmethod
    def clear(self):
        """Отчистить список."""
    
    # предусловие: список пуст
    # постусловие: в список добавляется первый узел с заданным значением
    @abc.abstractmethod
    def add_to_empty(self, value: T):
        """Добавить новый узел с заданным значением в пустой список"""
    
    # постусловие: в список добавляется первый узел с заданным значением
    @abc.abstractmethod
    def add_tail(self, value: T):
        """Добавить новый узел с заданным значением в хвост списка"""

    # предусловие: список не пуст
    # постусловие: для текущего узла заменяется значение на заданное
    @abc.abstractmethod
    def replace(self, value: T):
        """Заменить значение текущего узла на заданное"""

    # предусловие: список не пуст
    # постусловие: удаляются все узлы с заданным значением
    @abc.abstractmethod
    def remove_all(self, value: T):
        """Удалить все узлы с заданным значением"""
    
    # предусловие: список не пуст
    # постусловие: курсор устанавливается на узел с искомым значением
    @abc.abstractmethod
    def find(self):
        """Установить курсор на следующий узел с искомым значением"""

    # запросы

    # предусловие: список не пуст
    @abc.abstractmethod
    def get(self) -> T:
        """Получить значение текущего узла"""

    @abc.abstractmethod
    def size(self) -> int:
        """Получить количество узлов в списке"""

    @abc.abstractmethod
    def is_head(self) -> int:
        """Находится ли курсор в начале списка?"""

    @abc.abstractmethod
    def is_tail(self) -> int:
        """Находится ли курсор в конце списка?"""

    @abc.abstractmethod
    def is_value(self) -> int:
        """Установлен ли курсор на какой-либо узел?"""

    # дополнительные запросы
    @abc.abstractmethod
    def get_head_status() -> int:
        """Получить статус выполнения команды head. Возвращает значение HEAD_*"""

    @abc.abstractmethod
    def get_tail_status() -> int:
        """Получить статус выполнения команды tail. Возвращает значение TAIL_*"""

    @abc.abstractmethod
    def get_right_status() -> int:
        """Получить статус выполнения команды right. Возвращает значение RIGHT_*"""

    @abc.abstractmethod
    def get_get_status() -> int:
        """Получить статус выполнения запроса get. Возвращает значение GET_*"""

    @abc.abstractmethod
    def get_put_right_status() -> int:
        """Получить статус выполнения команды puh_right. Возвращает значение PUT_RIGHT_*"""

    @abc.abstractmethod
    def get_put_left_status() -> int:
        """Получить статус выполнения команды put_left. Возвращает значение PUT_LEFT*"""

    @abc.abstractmethod
    def get_remove_status() -> int:
        """Получить статус выполнения команды remove. Возвращает значение REMOVE_*"""

    @abc.abstractmethod
    def get_add_to_empty_status() -> int:
        """Получить статус выполнения команды add_to_empty. Возвращает значение ADD_TO_EMPTY_*"""

    @abc.abstractmethod
    def get_replace_status() -> int:
        """Получить статус выполнения команды replace. Возвращает значение REPLACE_*"""

    @abc.abstractmethod
    def get_find_status() -> int:
        """Получить статус выполнения команды find. Возвращает значение FIND_*"""

    @abc.abstractmethod
    def get_remove_all_status() -> int:
        """Получить статус выполнения команды remove_all. Возвращает значение REMOVE_ALL*"""
