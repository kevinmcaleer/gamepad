from time import sleep
from machine import PWM, Pin 

class Motor:
    """
    A class to represent a motor controlled via the DRV8833 driver.

    Attributes:
        in1 (Pin): The first input pin for motor control.
        in2 (PWM): The second input pin (PWM) for speed control.
    """

    def __init__(self, in1_pin: int, in2_pin: int):
        """
        Initializes the motor with specified input pins.

        Args:
            in1_pin (int): The GPIO pin number for input 1 (direction).
            in2_pin (int): The GPIO pin number for input 2 (PWM control).
        """
        self.in1 = Pin(in1_pin, Pin.OUT)
        self.in2 = PWM(Pin(in2_pin))
        self.in2.freq(1000)  # Set PWM frequency to 1kHz

    def speed(self, value: float):
        """
        Sets the motor speed and direction.

        Args:
            value (float): Speed value (-1 to 1). Negative values reverse direction.
        """
        if value < 0:
            self.in1.low()  # Reverse direction
        else:
            self.in1.high()  # Forward direction
        self.in2.duty_u16(int(abs(value) * 65535))  # Set PWM duty cycle (0-65535)

    def brake(self):
        """
        Brakes the motor by setting both inputs HIGH.
        """
        self.in1.high()
        self.in2.duty_u16(65535)

    def coast(self):
        """
        Coasts the motor by setting both inputs LOW.
        """
        self.in1.low()
        self.in2.duty_u16(0)

# setup motors
motor_a = Motor(6,7)
motor_b = Motor(27,26)

# move motors
speed = 1.0

print(f"speed = {speed}")

motor_a.speed(speed)
motor_b.speed(speed)

sleep(1)

# stop motors
print("stoping motor")
motor_a.coast()
motor_b.coast()