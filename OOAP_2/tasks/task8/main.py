from typing import Generic, TypeVar
from dataclasses import dataclass

# Пример ковариантности
class Animal:
    def voice(self) -> None:
        print("basic animal voice")

class Dog(Animal):
    def voice(self) -> None:
        print("Gav")

class Cat(Animal):
    def voice(self) -> None:
        print("Meow")

animal_type = TypeVar("animal_type", covariant=True)

@dataclass
class HouseWithAnimal(Generic[animal_type]):
    animal: animal_type

HouseWA = HouseWithAnimal[Animal]
house_with_cat = HouseWA(Cat())


# Пример контравариантности

armor = TypeVar("armor", contravariant=True)

@dataclass
class ContravariantArmor(Generic[armor]): 
    item: armor

class Armor: pass
class LeatherArmor(Armor): pass
class HeavyArmor(Armor): pass
class LightArmor(Armor): pass
class MetalCuirass(HeavyArmor):pass

def take_heavy_armor_damage(armor: ContravariantArmor[HeavyArmor]) -> None: pass

ha = ContravariantArmor(HeavyArmor())
take_heavy_armor_damage(ha)
a = ContravariantArmor(Armor())
take_heavy_armor_damage(a)

mc = ContravariantArmor(MetalCuirass())
take_heavy_armor_damage(mc)

