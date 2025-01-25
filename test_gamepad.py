# Example usage:

import asyncio
from gamepad_server import GamePadServer
# from burgerbot import Burgerbot

# robot = Burgerbot()
gamepad = GamePadServer()
asyncio.run(gamepad.main())

print('checking for commands')
while True:
    if gamepad.is_up:
#         robot.forward()
        print('robot forward')
    elif gamepad.is_down:
        print('robot backward')
#         robot.backward()
    elif gamepad.is_left:
#         robot.turn_left()
        print('robot left')
    elif gamepad.is_right:
        print('robot right')
# robot.turn_right()
#     elif gamepad.none:
        
#         robot.stop()