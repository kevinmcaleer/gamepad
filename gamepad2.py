import machine
import aioble
import asyncio
from micropython import const
import bluetooth
from time import ticks_ms, ticks_diff

class Button:
    def __init__(self, pin: int, debounce_ms: int = 50):
        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.debounce_ms = debounce_ms
        self._last_pressed = 0

    async def is_pressed(self) -> bool:
        current_time = ticks_ms()
        if self.pin.value() == 0:  # Button pressed
            if ticks_diff(current_time, self._last_pressed) > self.debounce_ms:
                self._last_pressed = current_time
                return True
        return False

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


        print('GamePad initialized')

    async def monitor_buttons(self):
        """ Continuously check button states asynchronously """
        while True:
            for name, button in self.buttons.items():
                if await button.is_pressed():
                    print(f"Button {name} pressed")
                    if self.connection:
                        self.button_characteristic.write(name.encode())
                        self.button_characteristic.notify(self.connection, name.encode())
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
