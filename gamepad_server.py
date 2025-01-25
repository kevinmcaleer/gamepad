import machine
import asyncio

class GamePadServer:
    """ A class to handle BLE communication and interpret commands from a Bluetooth gamepad remote.

    Attributes:
        device_name (str): The name of the BLE device.
        led (Pin): Onboard LED for connection status indication.
        connected (bool): Tracks the connection status.
        connection (aioble.Connection): Active BLE connection.
        command (str): The last received command from the gamepad.
    """

    def __init__(self, device_name="KevsRobots"):
        """
        Initializes the BLE server with the specified device name.

        Args:
            device_name (str): The name of the BLE device to advertise.
        """
        import aioble
        import bluetooth
        from micropython import const

        self.device_name = device_name
        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.connected = False
        self.connection = None
        self.command = None

        # UUIDs and constants
        self._GENERIC = bluetooth.UUID(0x1848)
        self._BUTTON_UUID = bluetooth.UUID(0x2A6E)
        self._BLE_APPEARANCE_GENERIC_REMOTE_CONTROL = const(384)

        # Services and Characteristics
        self.remote_service = aioble.Service(self._GENERIC)
        self.button_characteristic = aioble.Characteristic(
            self.remote_service, self._BUTTON_UUID, read=True, notify=True
        )

        # Register the services
        aioble.register_services(self.remote_service)

    async def advertise(self):
        """
        Advertises the BLE service and waits for connections.
        """
        import aioble

        while True:
            self.connected = False
            async with await aioble.advertise(
                250_000,  # Advertisement interval
                name=self.device_name,
                appearance=self._BLE_APPEARANCE_GENERIC_REMOTE_CONTROL,
                services=[self._GENERIC],
            ) as self.connection:
                print("Connection from", self.connection.device)
                self.connected = True
                await self.connection.disconnected()
                print("Disconnected")

    async def read_commands(self):
        """
        Continuously reads commands from the gamepad and stores the latest command.
        """
        while True:
            if self.connected:
                # Read and decode the command from the characteristic
                command = self.button_characteristic.read()
                if command:
                    self.command = command.decode("utf-8").strip().lower()
                    print(f"Received command: {self.command}")

            await asyncio.sleep_ms(100)

    @property
    def is_up(self):
        """Returns True if the "up" command is received."""
        return self.command == "up"

    @property
    def is_down(self):
        """Returns True if the "down" command is received."""
        return self.command == "down"

    @property
    def is_left(self):
        """Returns True if the "left" command is received."""
        return self.command == "left"

    @property
    def is_right(self):
        """Returns True if the "right" command is received."""
        return self.command == "right"

    @property
    def none(self):
        """Returns True if no command is currently received."""
        return self.command is None

    async def blink_status(self):
        """
        Blinks the onboard LED to indicate connection status.
        """
        toggle = True
        while True:
            self.led.value(toggle)
            toggle = not toggle
            await asyncio.sleep_ms(1000 if self.connected else 250)

    async def main(self):
        """
        Runs the main tasks for the GamePadServer.
        """
        tasks = [
            asyncio.create_task(self.advertise()),
            asyncio.create_task(self.blink_status()),
            asyncio.create_task(self.read_commands()),
        ]
        await asyncio.gather(*tasks)

# Example usage:
# robot = Burgerbot()
# gamepad = GamePadServer()
# asyncio.run(gamepad.main())
#
# while True:
#     if gamepad.is_up:
#         robot.forward()
#     elif gamepad.is_down:
#         robot.backward()
#     elif gamepad.is_left:
#         robot.turn_left()
#     elif gamepad.is_right:
#         robot.turn_right()
#     elif gamepad.none:
#         robot.stop()

