# Начнем с наследования, без абстракных классов
class Animal:
    def voice(self) -> None:
        print("basic animal voice")

# Отнаследуемся собачкой и кошечкой
class Dog(Animal):
    def voice(self) -> None:
        print("Gav")

class Cat(Animal):
    def voice(self) -> None:
        print("Meow")


# Композиция, кошечка или собачка в домике
class HouseWithAnimal:
    animal: Animal

    def __init__(self, animal: Animal) -> None:
        self.animal = animal

    def sound_from_house(self) -> None:
        self.animal.voice()


# полиморфизм с наследованием
animals = [Cat(), Dog()]
for animal in animals:
    animal.voice() #  Meow, Gav

# полиморфизм с композицией
houses = [HouseWithAnimal(Cat()), HouseWithAnimal(Dog())]
for house in houses:
    house.sound_from_house() # Meow, Gav
