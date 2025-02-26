import abc
from typing import Generic, TypeVar

T = TypeVar("T")

class AbstractDynamicArray(Generic[T], abc.ABC):
    """АТД динамического массива"""

    REMOVE_OK = 0 # последний вызов remove() отработал нормально
    REMOVE_ERR = 1 # индекс за пределами размера массива

    SET_OK = 0 # последний вызов set() отработал нормально
    SET_ERR = 1 # индекс за пределами размера массива

    SWAP_OK = 0 # последний вызов swap() отработал нормально
    SWAP_LEFT_OUT_OF_RANGE = 1 # левый индекс за пределами размера массива
    SWAP_RIGHT_OUT_OF_RANGE = 1 # правый индекс за пределами размера массива

    RESERVE_OK = 0 # последний вызов reserve() отработал нормально
    RESERVE_ERR = 1 # В системе отсутствует свободная память нужного объема

    GET_OK = 0 # последний вызов get() отработал нормально
    GET_ERR = 1 # индекс за пределами размера массива

    FIND_OK = 0 # последний вызов find() отработал нормально
    FIND_ERR = 1 # индекс за пределами размера массива

    # конструктор
    def __init__(self, size: int = 16) -> None:

    # Команды
    
    #постусловие: в конец массива добавлен элемент с заданным значением
    @abc.abstractmethod
    def append(self, value: T) -> None:
        """Добавить элемент в  конец списка"""

    #предусловие: индекс находится в пределах размера массива
    #постусловие: элемент массива с заданным индексом удален
    @abc.abstractmethod
    def remove(self, index: int) -> None:
        """Удалить элемент по индексу"""

    #постусловие: Удаляет все элементы массива без освобождения памяти
    @abc.abstractmethod
    def clear(self) -> None:
        """Отчистить список"""

    #предусловие: индекс находится в пределах размера массива
    #постусловие: элементу массива с заданным индексом присваивается новое значение
    @abc.abstractmethod
    def set(self, index: int, value: T) -> None:
        """Установить значение в массиве по заданому индексу"""

    #предусловие: индексы находится в пределах размера массива
    #постусловие: элементы по заданым индексам поменяны местами
    @abc.abstractmethod
    def swap(self, left: int, right: int) -> None:
        """Поменять элементы местами по индексам"""

    #предусловие: в системе присутствует требуемый объем памяти
    #постусловие: размер хранилища увеличен
    @abc.abstractmethod
    def reserve(self, new_size: int) -> None:
        """Выделить новый объем памяти для хранилища"""
    
    # Запросы
    
    #предусловие: индекс находится в пределах размера массива
    @abc.abstractmethod
    def get(self, index: int) -> None:
        """Получить элемент по индексу"""

    #предусловие: индекс, с которого ведется поиск, находится впределах размера массива
    @abc.abstractmethod
    def find(self, value: T, begin_from: int = 0) -> int:
        """Получить индекс первого элемента с заданным значением."""

    @abc.abstractmethod
    def size(self) -> int:
        """Запрос количества элементов в массиве"""

    @abc.abstractmethod
    def capacity(self) -> int:
        """Запрос размера текущего выделенного хранилища"""
    
    # Дополнительные запросы
    

    @abc.abstractmethod
    def get_remove_status() -> int:
        """Получить статус выполнения команды remove. Возвращает значение REMOVE_*"""

    @abc.abstractmethod
    def get_set_status() -> int:
        """Получить статус выполнения команды set. Возвращает значение SET_*"""

    @abc.abstractmethod
    def get_reserve_status() -> int:
        """Получить статус выполнения команды reserve. Возвращает значение RESERVE_*"""

    @abc.abstractmethod
    def get_swap_status() -> int:
        """Получить статус выполнения команды swap. Возвращает значение SWAP_*"""

    @abc.abstractmethod
    def get_get_status() -> int:
        """Получить статус выполнения команды get. Возвращает значение GET_*"""

    @abc.abstractmethod
    def get_find_status() -> int:
        """Получить статус выполнения команды find. Возвращает значение FIND_*"""
