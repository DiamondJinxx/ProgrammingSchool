import abc
class Animal:

    @abc.abstractmethod
    def voice(self) -> None:
        ...

class Dog(Animal):
    def voice(self) -> None:
        print("Gav")

class Cat(Animal):
    def voice(self) -> None:
        print("Meow")


animal: Animal = Dog()
animal.voice()
