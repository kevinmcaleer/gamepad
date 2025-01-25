# Checks to see if start button pressed down at boot, if so exits to REPL

from machine import Pin

start = Pin(12, Pin.IN, Pin.PULL_UP) 

if start.value() == 0:
    print("Start button pressed. Exiting...")
    import sys
    sys.exit()
else:
    print("Start button not pressed. Continuing...")