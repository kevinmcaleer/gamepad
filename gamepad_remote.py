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


class GamePad():
    def __init__(self):
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

        self.MANUFACTURER_ID = const(0x02A29)
        self.MODEL_NUMBER_ID = const(0x2A24)
        self.SERIAL_NUMBER_ID = const(0x2A25)
        self.HARDWARE_REVISION_ID = const(0x2A26)
        self.BLE_VERSION_ID = const(0x2A28)

        self.led = machine.Pin("LED", machine.Pin.OUT)

        self._ENV_SENSE_UUID = bluetooth.UUID(0x180A)
        self._GENERIC = bluetooth.UUID(0x1848)
        self._ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x1800)
        self._BUTTON_UUID = bluetooth.UUID(0x2A6E)

        self._BLE_APPEARANCE_GENERIC_REMOTE_CONTROL = const(384)

        # Advertising frequency
        self.ADV_INTERVAL_MS = 250_000

        self.device_info = aioble.Service(self._ENV_SENSE_UUID)

        # Setup OLED
        id = 0
        sda = 0
        scl = 1
        i2c = I2C(sda=sda,scl=scl, id=id)
        self.oled = SSD1306_I2C(128,64,i2c)
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
                    self.oled.clear()
                    self.oled.text(f"{name} down",0,0)
                    self.oled.show()
                    if self.connection:
                        self.button_characteristic.write(f"{name}_down".encode())
                        self.button_characteristic.notify(self.connection, f"{name}_down".encode())
                elif button_up:
                    print(f"Button {name} released")
                    self.oled.clear()
                    self.oled.text(f"{name} up",0,0)
                    self.oled.show()
                    if self.connection:
                        self.button_characteristic.write(f"{name}_up".encode())
                        self.button_characteristic.notify(self.connection, f"{name}_up".encode())
            await asyncio.sleep_ms(10)


    async def peripheral_task(self):
        """ Handle BLE advertising and connections """
        print("Peripheral task started")
        while True:
            self.connected = False
            async with await aioble.advertise(
                self.ADV_INTERVAL_MS,
                name="KevsRobots",
                appearance=self._BLE_APPEARANCE_GENERIC_REMOTE_CONTROL,
                services=[self._ENV_SENSE_TEMP_UUID],
            ) as self.connection:
                print("Connection from", self.connection.device)
                self.connected = True
                await self.connection.disconnected()
                print("Disconnected")

    async def blink_task(self):
        """ Blink the LED to indicate connection status """
        print("Blink task started")
        while True:
            self.led.toggle()
            blink_interval = 250 if not self.connected else 1000
            await asyncio.sleep_ms(blink_interval)

    async def main(self):
        """ Run all tasks concurrently """
        tasks = [
            asyncio.create_task(self.peripheral_task()),
            asyncio.create_task(self.blink_task()),
            asyncio.create_task(self.monitor_buttons()),
        ]
        await asyncio.gather(*tasks)

    def begin(self):
        """ Start the gamepad """
        print("GamePad starting")
        asyncio.run(self.main())
