import machine
import aioble
import asyncio
from micropython import const
import bluetooth
from time import ticks_ms, ticks_diff
from ssd1306 import SSD1306_I2C
from machine import I2C

class Button:
    def __init__(self, pin: int, debounce_ms: int = 50):
        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.debounce_ms = debounce_ms
        self._last_pressed = ticks_ms()
        self._was_pressed = False

    async def is_pressed(self) -> bool:
        current_time = ticks_ms()
        if self.pin.value() == 0:  # Button is pressed
            if ticks_diff(current_time, self._last_pressed) > self.debounce_ms:
                self._last_pressed = current_time
                return True
        return False

    async def state_changed(self) -> tuple[bool, bool]:
        """Check for button press/release events."""
        is_pressed = self.pin.value() == 0
        if is_pressed and not self._was_pressed:  # Button down
            self._was_pressed = True
            return True, False
        elif not is_pressed and self._was_pressed:  # Button up
            self._was_pressed = False
            return False, True
        return False, False

class GamePad:
    def __init__(self, gamepad_server):
        self.buttons = {
            "A": Button(6),
            "B": Button(7),
            "X": Button(4),
            "Y": Button(5),
            "Up": Button(8),
            "Down": Button(9),
            "Left": Button(2),
            "Right": Button(3),
            "Start": Button(12),
            "Select": Button(11),
            "Menu": Button(10),
        }
        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.connected = False
        self.connection = None
        self.gamepad_server = gamepad_server  # Link to GamePadServer instance

        # Setup OLED
        id = 0
        sda = 0
        scl = 1
        i2c = I2C(sda=sda, scl=scl, id=id)
        self.oled = SSD1306_I2C(128, 64, i2c)
        self.oled.text("GamePad", 0, 0)
        self.oled.show()

        print('GamePad initialized')

    async def monitor_buttons(self):
        """ Continuously check button states asynchronously """
        while True:
            for name, button in self.buttons.items():
                button_down, button_up = await button.state_changed()
                if button_down:
                    print(f"Button {name} pressed down")
                    self.oled.fill(0)  # Clear OLED
                    self.oled.text(f"{name} down", 0, 0)
                    self.oled.show()
                    if self.gamepad_server.connected:
                        self.gamepad_server.button_characteristic.write(f"{name}_down".encode())
                        self.gamepad_server.button_characteristic.notify(
                            self.gamepad_server.connection, f"{name}_down".encode()
                        )
                elif button_up:
                    print(f"Button {name} released")
                    self.oled.fill(0)  # Clear OLED
                    self.oled.text(f"{name} up", 0, 0)
                    self.oled.show()
                    if self.gamepad_server.connected:
                        self.gamepad_server.button_characteristic.write(f"{name}_up".encode())
                        self.gamepad_server.button_characteristic.notify(
                            self.gamepad_server.connection, f"{name}_up".encode()
                        )
            await asyncio.sleep_ms(10)
