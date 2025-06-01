from typing import Self, final
import copy
import pickle

class __General:
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
        return str(self)

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



class AnyObj(__General):
    """Класс доступный для модификации."""


class MyNone(AnyObj):
    """Замыкание системы типов снизу"""

