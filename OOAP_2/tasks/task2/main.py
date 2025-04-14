from dataclasses import dataclass

# Пусть у нас будет небольшой проект игры в жанре гоночек.

# Класс для реализации колес на машинах.
@dataclass
class Wheel:
    """Базовый класс колеса."""
    radius: int


# Расширим колесо для зимы - сделаем зимнее колесо.
@dataclass
class WinterWheel(Wheel):
    """Зимнее колесо"""

# Специализируем зимнее колесо - сделаем его шипованным. Так же бывают колеса-липучки, это отдельная специализация.
@dataclass
class StuddedWheel(WinterWheel):
    """Шипованное колесо"""
    spike_protrusion: int
    spike_count: int
