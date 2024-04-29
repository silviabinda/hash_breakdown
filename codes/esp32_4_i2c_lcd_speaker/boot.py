# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

'''
SPDX-FileCopyrightText: © 2024 Silvia Binda Heiserova silviaheiserova@gmail.com

SPDX-License-Identifier: MIT

This code is part of "Hash Breakdown" by Silvia Binda Heiserova, 2024

This code is run on ESP32 WROOM microcontroller conected to the I2C LCD display (16x2).
Description of connections:

I2C LCD display has assigned following esp32 pins:
SDA (violet wire) = (esp32 GPIO21)
SCL (grey wire) = (esp32 GPIO22)
GND (black wire) = (connected to GND) 
VCC (red wire) = (connected to VIN)

!!!!! When externally powered, I2C LCD display and ESP32 need to have a common Ground for correct communication !!!

ESP32 info for router:
Device Name: mpy-esp32
MAC Address: 24-DC-C3-9F-D3-8C
Reserved IP Address: 192.168.0.102
________________________________________________________________________________________________________________

'''

# This file is executed on every boot (including wake-boot from deepsleep)

import machine
import _thread
import time
import random
from machine import Pin, SoftI2C
import offline_router # our .py code for connection to wifi router 
from i2c_lcd import I2cLcd
from time import sleep                                                                              
from socket import * # library for network communication

s = socket (AF_INET, SOCK_DGRAM) # udp network connection (is more fast but less reliable, which in our case is the best solution)
esp32_i2c_lcd = ('192.168.0.102',8345) # ip address of esp32_1 (this esp32 connected to oled and us sensor), will never change as we are using an offline router with assigned ip adresses
s.bind(esp32_i2c_lcd)
dir = ('192.168.0.199', 8345) # ip address of pc 

# Onboard led
ledPin = machine.Pin(2, machine.Pin.OUT)

# Define speaker pin
SPEAKER_PIN = 26

# Set up PWM for the speaker
speaker = machine.PWM(machine.Pin(SPEAKER_PIN), freq=440, duty=512)  # Initialize with some default values

# Define a combined melody pattern (frequency in Hz and duration in milliseconds)
base_melody = [
    (440, 200), (880, 200), (440, 200), (880, 200),  # Classic rising and falling tone
    (523, 200), (659, 200), (784, 200), (1047, 400), # Part of a scale
    (784, 200), (659, 200), (523, 200), (440, 400),  # Descending scale
    (392, 300), (392, 300), (440, 300), (440, 300),  # Zelda-inspired smooth flow
    (494, 300), (494, 300), (440, 600),              # Rising action
    (330, 300), (294, 300), (262, 600)               # Calm, descending back
]

# Add abstract randomness to the melody
random_bits = [(random.randint(200, 1000), random.randint(100, 400)) for _ in range(5)]
combined_melody = base_melody + random_bits

#define the I2C LCD display address, number of raws and columns
I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000) #initializing the I2C method for ESP32
#i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)       #initializing the I2C method for ESP8266

lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)
backlight = True # Turns on the backlight of the LCD

# Define a global flag to indicate when TextNumInfo() is done
text_num_info_done = True

#Function for receiving messages from PC: 
def recmessage():
    while True:
        message, dir = s.recvfrom(1024) # to receive the message from the pc
        #sleep(2)
        print(message, dir)
        return message

def display_message_segments(pause=2):
    while True:
        ledPin.value(1)
        lcd.putstr("...processing...")
        message = recmessage().decode("utf-8") #uncomment for exhibition
        #message = "Hello, world! This is a test message using both rows of your I2C LCD display. Enjoy!" #comment for exhibition
        print("diplay_message_segment is running" )
        lcd.clear()
        if len(message)>16:
            play_and_clear()
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
            lcd.clear()
        else:
            lcd.putstr("...processing...")
            sleep(0.01)

def play_melody():
    start_time = time.ticks_ms()
    for freq, dur in combined_melody:
        speaker.freq(freq)  # Set frequency
        speaker.duty(56)   # Set duty cycle to about 25% for a moderate sound
        time.sleep_ms(dur)  # Duration of the note
        speaker.duty(0)     # Silence between notes
        if time.ticks_diff(time.ticks_ms(), start_time) > 10000:  # Stop after 10 seconds
            break
        time.sleep_ms(50)   # Short pause between notes to maintain the rhythm

def play_and_clear():
    play_melody()
    # Clean up by stopping PWM
    speaker.deinit

def TextNumInfo():
    while True:
        ledPin.value(1)
        lcd.putstr("...processing...")
        message = recmessage().decode("utf-8")
        print("TextNumInfo is running") # to check if the function is running 
        lcd.clear()
        
        # Implement right-to-left scrolling effect
        if len(message) > totalColumns:
            # Add padding spaces so that the text scrolls in from the right completely
            padded_message = ' ' * totalColumns + message + ' ' * totalColumns
            # Scroll from right to left
            for i in range(len(message) + totalColumns):
                start_index = len(padded_message) - totalColumns - i
                display_text = padded_message[start_index:start_index + totalColumns]
                lcd.move_to(0, 0)
                lcd.putstr(display_text)
                time.sleep(0.05)  # Adjust this delay to control scroll speed
        else:
            lcd.move_to(0, 0)
            lcd.putstr(message)
            time.sleep(15)  # Time to display static message before clearing or receiving new one

        lcd.clear()
    
try:
    display_message_segments(3)
except Exception as e:
    print(e)

# many thanks to the tutorial: https://microcontrollerslab.com/i2c-lcd-esp32-esp8266-micropython-tutorial/
# LCD custom character generator: https://maxpromer.github.io/LCD-Character-Creator/
# (choose the interfacing "I2C" and the Data Type "Hex")