# Kevin McAleer
# 22 January 2025
# Button Test

import asyncio
from gamepad import GamePad

async def test_gamepad():
    gamepad = GamePad()
    print("Starting gamepad")
    await asyncio.gather(
        gamepad.main(),  # Run the gamepad's main tasks
        monitor_start_button(gamepad)  # Monitor for the start button press
    )

async def monitor_start_button(gamepad):
    """Exit the program when the start button is pressed."""
    while True:
        if await gamepad.buttons["Start"].is_pressed():  # Await the asynchronous method
            print("Start button pressed. Exiting...")
            break
        await asyncio.sleep(0.1)  # Avoid busy-waiting

if __name__ == "__main__":
    asyncio.run(test_gamepad())
