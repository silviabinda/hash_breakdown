import machine
from machine import Pin, SoftI2C
from i2c_lcd import I2cLcd
from time import sleep                                                                            
from socket import *

I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)  # initializing the I2C method for ESP32
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)
backlight = True  # Turns on the backlight of the LCD

def display_message_segments(message, pause=2):
    display_capacity = totalRows * totalColumns  # Total characters display can show at one time
    parts = [message[i:i + display_capacity] for i in range(0, len(message), display_capacity)]
    
    for part in parts:
        lcd.clear()
        # Display up to 16 characters on the first row
        lcd.putstr(part[:totalColumns])
        # If there's more to display, put the rest on the second row
        if len(part) > totalColumns:
            lcd.move_to(0, 1)  # Move cursor to the beginning of the second row
            lcd.putstr(part[totalColumns:totalColumns * 2])
        sleep(pause)

# Example usage
display_message_segments("Hello, world! This is a test message using both rows of your I2C LCD display. Enjoy!", 3)
