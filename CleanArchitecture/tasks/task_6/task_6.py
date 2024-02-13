from dataclasses import dataclass, field
from enum import Enum


from .pure_robot import *


class State(Enum):
    WATER = 1 # полив водой
    SOAP  = 2 # полив мыльной пеной
    BRUSH = 3 # чистка щётками


@dataclass
class Robot:
    transfer: callable = field(default=transfer_to_cleaner)
    state: RobotState = field(default_factory=lambda: RobotState(0, 0, 0, State.WATER)) 

    def move(self, dist) -> RobotState:
        self.state = move(self.transfer, dist, self.state)
        return self.state

    def turn(self, angle) -> RobotState:
        self.state = turn(self.transfer, angle, self.state)
        return self.state

    def set_state(self, new_state) -> RobotState:
        self.state = set_state(self.transfer, new_state, self.state)
        return self.state

    def start(self) -> RobotState:
        self.state = start(self.transfer, self.state)
        return self.state

    def stop(self) -> RobotState:
        self.state = stop(self.transfer, self.state)
        return self.state

    def make(self, code) -> RobotState:
        return make(self.transfer, code)


def main():
    robot = Robot()
    robot.make(
        (
            'move 100',
            'turn -90',
            'set soap',
            'start',
            'move 50',
            'stop'
        ), 
    )

main()
