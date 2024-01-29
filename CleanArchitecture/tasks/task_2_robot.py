import math

x: int = 0
y: int = 0
angle: int = 0
state: str = ''

def start() -> None:
    print(f"START WITH {state}")

def my_set(new_state: str) -> None:
    valid_state = ['water', 'soap', 'brush']
    new_state = str(new_state)
    global state
    if new_state not in valid_state:
        return
    state = new_state
    print(f"STATE {state}")

def stop() -> None:
    print("STOP")

def turn(new_angle: int) -> None:
    global angle
    new_angle = int(new_angle)
    angle = new_angle
    print(f"ANGLE {angle}")

def move(meters: int) -> None:
    meters = int(meters)
    global x
    global y
    x = x + int(meters * math.cos(math.radians(angle)))
    y = y + int(meters * math.sin(math.radians(angle)))
    print(f"POS {x},{y}")

def execute_command(command_with_params: list[str]) -> None:
    command_mapping = {
        'move': move,
        'set': my_set,
        'stop': stop,
        'start': start,
        'turn': turn,
    }
    command = command_mapping.get(command_with_params[0])
    if command is None:
        return
    command(*command_with_params[1:])

def main():
    while True:
        source_command = str(input())
        command_with_params = source_command.split()
        execute_command(command_with_params)


main()