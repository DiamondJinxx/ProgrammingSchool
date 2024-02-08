from .robot import robot

def main():
    while True:
        source_command = str(input())
        command_with_params = source_command.split()
        robot.execute_command(command_with_params)
        
        
main()