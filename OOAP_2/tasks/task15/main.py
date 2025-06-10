# Люблю я животных, что поделать :)
from enum import Enum
from dataclasses import dataclass, field

# реализация иерархии животных с идентификацией вида по полю
class AnimalType(Enum):
    """Вид животного"""
    CAT = "cat"
    DOG = "dog"


@dataclass(frozen=True)
class Animal:
    _type_of: AnimalType = field()

    def voice(self) -> None:
        # та самая логика, базирующаяся на типе
        voice_str = "I don't know who I am..."
        if self._type_of == AnimalType.CAT:
            voice_str = "moew"
        if self._type_of == AnimalType.DOG:
            voice_str = "gav"
        print(voice_str)



# плюс место для очень обидных очепяток - хотим создать кота, а создаем собаку или еще кого
cat = Animal(AnimalType.CAT)
cat.voice()

dog = Animal(AnimalType.DOG)
dog.voice()

humster = Animal("Humster")
humster.voice()


# реализация наследованием
class AnimalInheritance:
    def voice(self) -> None:
        print("basic animal voice")


class Dog(AnimalInheritance):
    def voice(self) -> None:
        print("Gav")


class Cat(AnimalInheritance):
    def voice(self) -> None:
        print("Meow")


cat = Cat()
cat.voice()

dog = Dog()
dog.voice()


# добавим отдельно и будет хомячок
# humster = Humster()
# humster.voice()
