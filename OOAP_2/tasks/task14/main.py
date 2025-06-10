import operator
from typing import Self, final, TypeVar, Generic
import copy
import pickle

T = TypeVar("T")

class __General(Generic[T]):
    """Базовый класс, закрытый от изменений."""

    @final
    def copy(self) -> Self:
        """Копирование объекта"""
        return copy.copy(self)

    @final
    def deep_copy(self) -> Self:
        """Глубокое копирование объекта"""
        return copy.deepcopy(self)

    @final
    def __eq__(self, value: object, /) -> bool:
        """Сравнение объектов на равенство."""
        return self == value

    @final
    def __repr__(self) -> str:
        return str(vars(self))

    @final
    def serialize(self) -> bytes:
        """Сериализация объекта."""
        return pickle.dumps(self)

    @final
    @classmethod
    def deserialize(cls, obj: bytes) -> Self:
        """Десериализация объекта."""
        return pickle.loads(obj)

    @final
    def is_type(self, type_: object) -> bool:
        """Проверка типа."""
        return type(self) is type_

    @final
    def get_type(self) -> object:
        """Получение типа объекта"""
        return type(self)

    @classmethod
    def assigment_attempt(cls, source, target) -> object:
        if type(source) is not type(target):
            target = MyNone()
            return target
        target = source
        return target



class AnyObj(__General[T]):
    """Класс доступный для модификации."""

    def __add__(self, other: Self) -> Self:
        """Сложение объектов"""
        raise NotImplementedError()


class MyNone(AnyObj[T]):
    """Замыкание системы типов снизу"""


class Vector(AnyObj[T]):
    seq: list[T]

    def __init__(self, *args: T, **kwargs) -> None:
        self.seq = args
        self._size = len(args)
    
    def __add__(self, other: Self) -> Self | MyNone:
        if self._size != len(other.seq):
            return MyNone()
        result = list(map(operator.add, self.seq, other.seq))
        return Vector(*result)


v1 = Vector[int](1,2,3,4)
print(v1)
v2 = Vector[int](1,2,3,4)
print(v1 + v2)

v1 = Vector[Vector[Vector[int]]](
    Vector[Vector[int]](
        Vector[int](1,2,3),
        Vector[int](4,5,6),
    ),
    Vector[Vector[int]](
        Vector[int](7,8,9),
        Vector[int](10,11,12),
    ),
)

v2 = Vector[Vector[Vector[int]]](
    Vector[Vector[int]](
        Vector[int](1,2,3),
        Vector[int](4,5,6),
    ),
    Vector[Vector[int]](
        Vector[int](7,8,9),
        Vector[int](10,11,12, 13),
    ),
)

print(v1 + v2)
