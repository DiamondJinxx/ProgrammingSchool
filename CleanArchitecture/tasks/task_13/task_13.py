import pure_robot


class RobotApi:

    def setup(self, f_make):
        self.f_make = f_make

    def __call__(self, command):
        if not hasattr(self, 'cleaner_state'):
            self.cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)
        self.result = self.f_make(command, self.cleaner_state)
        return self.result


def is_command(string: str) -> bool:
    """Check string is robot command"""
    commands = ('move','turn', 'set', 'start', 'stop')
    return string in commands


def custom_make(command, state) -> tuple[str, pure_robot.RobotState]:
        tokens = command.split(' ')
        result = ('', state)
        for token in tokens:
            if not is_command(token):
                pure_robot.ARG_STACK.append(token)
                continue
            if token=='move':
                result = pure_robot.move(result[1]) 
            elif token=='turn':
                result = pure_robot.turn(result[1])
            elif token=='set':
                result = pure_robot.set_state(result[1]) 
            elif token=='start':
                result = pure_robot.start(result[1])
            elif token=='stop':
                result = pure_robot.stop(result[1])
        return result


api = RobotApi()
api.setup(custom_make)