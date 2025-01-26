# Gamepad

This is a simple gamepad library for MicroPython. It is designed to be used with the kevsrobots.com/gamepad.

[Functional Reference](functional_reference.md)

---

## Code Examples

1. `test_buttons.py` - example code for the GamePad remote control
2. `test_oled.py` - example of using the OLED display
3. `test_motor_shim.py` - example for a pico robot that uses the Pimoroni Motor Shim to control 2 motors

---

## Supporting files

1. `burgerbot.py` - Provides movement code for a [BurgerBot](https://www.kevsrobots.com/burgerbot) robot
2. `boot.py` - save this on the GamePad if you want to easily exit out of the example code by holding down the Start Menu when you power it up.
3. `motor.py` - a small but handy class for modelling simple motors
4. `ssd1306.py` - OLED display driver, use this on the gamepad to write text and clear the screen.
