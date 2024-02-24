import abc
import math
from dataclasses import dataclass

@dataclass
class AbstractRobot(abc.ABC):

    @abc.abstractmethod
    def start(self) -> None:
        pass

    @abc.abstractmethod
    def my_set(self, state: str) -> None:
        pass

    @abc.abstractmethod
    def stop(self) -> None:
        pass

    @abc.abstractmethod
    def turn(self, angle: int) -> None:
        pass

    @abc.abstractmethod
    def move(self, meters: int) -> None:
        pass




@dataclass
class Robot(AbstractRobot):
    x: int = 0
    y: int = 0
    angle: int = 0
    state: str = ''
    _valid_state = ['water', 'soap', 'brush']

    def start(self) -> None:
        print(f"START WITH {self.state}")

    def my_set(self, state: str) -> None:
        state = str(state)
        if state not in self._valid_state:
            return
        self.state = state
        print(f"STATE {self.state}")

    def stop(self) -> None:
        print("STOP")

    def turn(self, angle: int) -> None:
        angle = int(angle)
        self.angle = angle
        print(f"ANGLE {self.angle}")

    def move(self, meters: int) -> None:
        meters = int(meters)
        self.x = self.x + int(meters * math.cos(math.radians(self.angle)))
        self.y = self.y + int(meters * math.sin(math.radians(self.angle)))
        print(f"POS {self.x},{self.y}")


def execute_command(robot, command_with_params):
    command_mapping = {
        'move': robot.move,
        'set': robot.my_set,
        'stop': robot.stop,
        'start': robot.start,
        'turn': robot.turn,
    }
    command = command_mapping.get(command_with_params[0])
    if command is None:
        return
    command(*command_with_params[1:])


def main():
    robot = Robot()
    while True:
        source_command = str(input())
        command_with_params = source_command.split()
        execute_command(robot, command_with_params)
        
        
main()