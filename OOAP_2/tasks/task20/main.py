import abc
# Наследование с функциональной вариацией
class Animal:
    def voice(self) -> None:
        print("basic animal voice")

class Dog(Animal):
    def voice(self) -> None:
        print("Gav")

class Cat(Animal):
    def voice(self) -> None:
        print("Meow")


# Наследование с вариацией типа
class Animal:
    def voice(self) -> None:
        print("basic animal voice")

class Dog(Animal):
    def voice(self, is_angry: bool) -> None:
        print_str = "Gav"
        if is_angry:
            print_str = "Angry Gav"
        print(print_str)

# Наследование с конкретизацией
class Animal(abc.ABC):

    @abc.abstractmethod
    def voice(self) -> None:
        pass


class Dog(Animal):
    def voice(self) -> None:
        print("Gav")


# Структурное наследование
class Animal:
    def voice(self) -> None:
        print("basic animal voice")

class MovableObject:
    def move(self, x: int, y: int) -> None:
        print(f"Move to point ({x}, {y})")

class Dog(Animal, MovableObject):
    def voice(self) -> None:
        print("Gav")


