class Humanoid: pass
class Human(Humanoid): pass
class Male(Human): pass
class Female(Human): pass
class Alien(Humanoid): pass

class Animal:
    def voice(self) -> None:
        print("basic animal voice")

    def meet_humanoid(self, humanoid: Humanoid) -> None:
        print(f"{type(self)} meet {type(humanoid)}")


class Dog(Animal):
    # полиморфный вызов
    def voice(self) -> None:
        print("Gav")


class Cat(Animal):
    def voice(self) -> None:
        print("Meow")


cat = Cat()
cat.voice()
cat.meet_humanoid(Human())
cat.meet_humanoid(Male())
cat.meet_humanoid(Female())
cat.meet_humanoid(Alien())
