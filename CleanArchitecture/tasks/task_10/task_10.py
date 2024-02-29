from .pure_robot import *


# таким образом передаем каждый метод робота отдельно
def call_robot(method, state, *args):
    return method(transfer_to_cleaner, *args, state=state)