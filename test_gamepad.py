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
        if gamepad.command is not None:
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
#     p_task = asyncio.create_task(gamepad.peripheral_task())
#     gamepad.tasks.append(p_task)
    gamepad.tasks.append(monitor)
    gamepad.tasks.append(blink)
    await gamepad.main()
    
#     print (f'gamepad tasks {gamepad.tasks}')
    # Run both tasks concurrently
#     await asyncio.gather(*gamepad.tasks)

# Run the main coroutine
while True:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
        import sys
        sys.exit()
