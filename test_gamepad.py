import asyncio
from gamepad_remote import GamePadServer

async def monitor_gamepad(gamepad):
    """
    Monitor the gamepad for commands and act on them.
    """
    
    while True:
#         print(f'Checking for commands...{gamepad.connected}')
        if gamepad.is_up:
            print('Robot forward')
        elif gamepad.is_down:
            print('Robot backward')
        elif gamepad.is_left:
            print('Robot left')
        elif gamepad.is_right:
            print('Robot right')
        else:
            pass
        await asyncio.sleep(0.25)  # Avoid tight looping
        print(f'command: {gamepad.command}')

async def main():
    """
    Run the gamepad server and command monitoring concurrently.
    """
    gamepad = GamePadServer()
    
    # Note: `gamepad.main()` internally does:
    #   - read_commands()
    #   - find_remote()
    #   - peripheral_task()
    # So we do NOT call them again here.
    
    blink = asyncio.create_task(gamepad.blink_task())
    monitor = asyncio.create_task(monitor_gamepad(gamepad))
    
    gamepad.tasks.append(monitor)
    gamepad.tasks.append(blink)
    await gamepad.main()
    
#     read_commands = asyncio.create_task(gamepad.read_commands())
#     find_remote = asyncio.create_task(gamepad.find_remote())
#     peripheral_task = asyncio.create_task(gamepad.peripheral_task())
#     gamepad.tasks.append(read_commands)
#     gamepad.tasks.append(find_remote)
#     gamepad.tasks.append(peripheral_task)
    
    print (f'gamepad tasks {gamepad.tasks}')
    # Run both tasks concurrently
    await asyncio.gather(*gamepad.tasks)

# Run the main coroutine
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Exiting...")
