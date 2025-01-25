# OLED Test
from machine import I2C
from ssd1306 import SSD1306_I2C

id = 0
sda = 0
scl = 1
i2c = I2C(sda=sda,scl=scl, id=id)
oled = SSD1306_I2C(128,64,i2c)

oled.text("GamePad 2.0",20,30)
oled.show()