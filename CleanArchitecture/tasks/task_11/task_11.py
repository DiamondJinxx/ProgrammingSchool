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


def custom_make(command, state) -> pure_robot.RobotState:
        cmd = command.split(' ')
        if cmd[0]=='move':
             state = pure_robot.move(transfer_to_cleaner, int(cmd[1]), state) 
        elif cmd[0]=='turn':
            state = pure_robot.turn(transfer_to_cleaner, int(cmd[1]), state)
        elif cmd[0]=='set':
            state = pure_robot.set_state(transfer_to_cleaner, cmd[1], state) 
        elif cmd[0]=='start':
            state = pure_robot.start(transfer_to_cleaner, state)
        elif cmd[0]=='stop':
            state = pure_robot.stop(transfer_to_cleaner, state)
        return state


api = RobotApi()
api.setup(custom_make)