import pure_robot

class RobotApi:

    def setup(self, f_make):
        self.f_make = f_make

    def __call__(self, command):
        if not hasattr(self, 'cleaner_state'):
            self.cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)
        self.cleaner_state = self.f_make(command, self.cleaner_state)
        return self.cleaner_state


def transfer_to_cleaner(message):
    print (message)


def is_command(string: str) -> bool:
    """Check string is robot command"""
    commands = ('move','turn', 'set', 'start', 'stop')
    return string in commands


def custom_make(command, state) -> pure_robot.RobotState:
        tokens = command.split(' ')
        stack = []
        for token in tokens:
            if not is_command(token):
                stack.append(token)
                continue
            if token=='move':
                state = pure_robot.move(transfer_to_cleaner, int(stack.pop()), state) 
            elif token=='turn':
                state = pure_robot.turn(transfer_to_cleaner, int(stack.pop()), state)
            elif token=='set':
                state = pure_robot.set_state(transfer_to_cleaner, stack.pop(), state) 
            elif token=='start':
                state = pure_robot.start(transfer_to_cleaner, state)
            elif token=='stop':
                state = pure_robot.stop(transfer_to_cleaner, state)
        return state


api = RobotApi()
api.setup(custom_make)