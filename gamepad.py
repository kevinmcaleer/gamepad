# Kevin McAleer
# 2025-01-22
# GamePad BLE Remote Control

import sys
import aioble
import bluetooth
import machine
import uasyncio as asyncio
from micropython import const

# GamePad GPIO to Button Mapping

# The GamePad is available from www.kevsrobots.com/pcbs

#  Button Up = 8
#  Button Down = 9
#  Button Left = 2
#  Button Right = 3
#  Button A = 6
#  Button B = 7
#  Button X = 4
#  Button Y = 5
#  Button Start = 12
#  Button Select = 11
#  Button Menu = 10

class Button():
    def __init__(self, pin:int):
        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        
    def read(self) -> bool:
        if self.pin.value() == 0:
            print('button pressed')
            return True
        else:
            # print('button not pressed')
            return False
    
    @property
    def is_pressed(self) -> bool:
        return self.read()


class GamePad():
    def __init__(self):
        self.button_a = Button(6)
        self.button_b = Button(7)
        self.button_x = Button(4)
        self.button_y = Button(5)
        self.button_up = Button(8)
        self.button_down = Button(9)
        self.button_left = Button(2)
        self.button_right = Button(3)
        self.button_start = Button(12)
        self.button_select = Button(11)
        self.button_menu = Button(10)
        print('GamePad initialised')

    def begin(self):
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

        self.connection = None

        # Create characteristics for device info
        aioble.Characteristic(self.device_info, bluetooth.UUID(self.MANUFACTURER_ID), read=True, initial="KevsRobotsRemote")
        aioble.Characteristic(self.device_info, bluetooth.UUID(self.MODEL_NUMBER_ID), read=True, initial="1.0")
        aioble.Characteristic(self.device_info, bluetooth.UUID(self.SERIAL_NUMBER_ID), read=True, initial=self.uid())
        aioble.Characteristic(self.device_info, bluetooth.UUID(self.HARDWARE_REVISION_ID), read=True, initial=sys.version)
        aioble.Characteristic(self.device_info, bluetooth.UUID(self.BLE_VERSION_ID), read=True, initial="1.0")

        self.remote_service = aioble.Service(self._GENERIC)

        self.button_characteristic = aioble.Characteristic(
            self.remote_service, self._BUTTON_UUID, read=True, notify=True
        )

        print('registering services')
        aioble.register_services(self.remote_service, self.device_info)

        self.connected = False
        asyncio.run(self.run())

    @property
    def left_is_pressed(self) -> bool:
        return self.button_a.is_pressed
    
    @property
    def right_is_pressed(self) -> bool:
        return self.button_a.is_pressed
    
    @property
    def up_is_pressed(self) -> bool:
        return self.button_a.is_pressed
    
    @property
    def down_is_pressed(self) -> bool:
        return self.button_a.is_pressed
    
    @property
    def a_is_pressed(self) -> bool:
        return self.button_a.is_pressed
    
    @property
    def b_is_pressed(self) -> bool:
        return self.button_a.is_pressed
    
    @property
    def x_is_pressed(self) -> bool:
        return self.button_a.is_pressed
    
    @property
    def y_is_pressed(self) -> bool:
        return self.button_a.is_pressed
    
    @property
    def start_is_pressed(self) -> bool:
        return self.button_a.is_pressed
    
    @property
    def select_is_pressed(self) -> bool:
        return self.button_a.is_pressed
    
    @property
    def menu_is_pressed(self) -> bool:
        return self.button_a.is_pressed
    
    def uid(self):
        """ Return the unique id of the device as a string """
        return "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(
            *machine.unique_id())

    async def remote_task(self):
        """ Send the event to the connected device """

        while True:
            if not connected:
                print('not connected')
                await asyncio.sleep_ms(1000)
                continue
            if self.button_a.read():
                print(f'Button A pressed, connection is: {connection}')
                self.button_characteristic.write(b"a")   
                self.button_characteristic.notify(connection,b"a")
            elif self.button_b.read():
                print('Button B pressed')
                self.button_characteristic.write(b"b")
                self.button_characteristic.notify(connection,b"b")
            elif self.button_x.read():
                print('Button X pressed')
                self.button_characteristic.write(b"x")
                self.button_characteristic.notify(connection,b"x")
            elif self.button_y.read():
                print('Button Y pressed')
                self.button_characteristic.write(b"y")
                self.button_characteristic.notify(connection,b"x")
            else:
                self.button_characteristic.write(b"!")
            await asyncio.sleep_ms(10)
            
    # Serially wait for connections. Don't advertise while a central is
    # connected.    
    async def peripheral_task(self):
        print('peripheral task started')
        global connected, connection
        while True:
            connected = False
            async with await aioble.advertise(
                self.ADV_INTERVAL_MS, 
                name="KevsRobots", 
                appearance=self._BLE_APPEARANCE_GENERIC_REMOTE_CONTROL, 
                services=[self._ENV_SENSE_TEMP_UUID]
            ) as connection:
                print("Connection from", connection.device)
                connected = True
                print(f"connected: {connected}")
                await connection.disconnected()
                print(f'disconnected')
            

    async def blink_task(self):
        print('blink task started')
        toggle = True
        while True:
            self.led.value(toggle)
            toggle = not toggle
            blink = 1000
            if self.connected:
                blink = 1000
            else:
                blink = 250
            await asyncio.sleep_ms(blink)
        
    async def main(self):
        tasks = [
            asyncio.create_task(self.peripheral_task()),
            asyncio.create_task(self.blink_task()),
            asyncio.create_task(self.remote_task()),
        ]
        await asyncio.gather(*tasks)

    async def run(self):
        asyncio.run(self.main())
