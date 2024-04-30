# THIS CODE IS EXECUTED FROM THE ESP32 HANDLING THE OLED DISPLAY
# it receives messages from the main code which has to be shown on oled display and is shown on the oled display
# also it turns a RGB LED on (the RGB LED is mounted on the back of the 3D print module with router)

# ESP32 data for router:
# mpy-esp32
# 24-DC-C3-9F-D4-8C
# 192.168.0.104

# Connecting OLED 0.91'to the esp32:
# SCL = GPIO22
# SDA = GPIO21
# VCC = 3.3V
# GND = GND

# Connecting RGB LED to the esp32:
# G = GPIO27
# B = GPIO26
# - = GND

from machine import Pin, SoftI2C, PWM
import ssd1306 # library for oled display
import time
from time import sleep
import offline_router # our .py code for connection to wifi router
from _thread import start_new_thread # library for threading                                                                                   
from socket import * # library for network communication

# for connection to the oled display:
i2c = SoftI2C(scl=Pin(22), sda=Pin(21)) # assigning pins of the ESP32 for connection with oled display
oled = ssd1306.SSD1306_I2C (128, 32, i2c)

# for receiving messages from the main code (messages to be shown on oled display)
s = socket (AF_INET, SOCK_DGRAM) # udp network connection (is more fast but less reliable, which in our case is the best solution)

# !!!
esp32_oled = ('192.168.0.104',8345) # ip address of this esp32 (this esp32 connected to oled display), will never change as we are using an offline router with assigned ip adresses
s.bind(esp32_oled)
#dir = ('192.168.0.199', 8345) # ip address of pc (raspberry pi) 

# defining a string variable and its initial value:
message = '...processing...' 

# Setup the PWM pins for RGB LED (we only use green and blue pins of the rgb led)
greenPin = PWM(Pin(27)) # Assuming GPIO 27 for the green LED
bluePin = PWM(Pin(26))  # Assuming GPIO 26 for the blue LED

# Initialize PWM frequency
greenPin.freq(500)
bluePin.freq(500)
bluePin.duty(300) #blue
greenPin.duty(50) #red

# function for recieving messages from server:
def recmensaje():
    global message, dir # global variables
    while True:
        message_oled, dir = s.recvfrom(1024) # to receive the message from the main code
        #sleep(2)
        print(message_oled, dir)
        message = message_oled
        print(message)

# function for showing the message on oled display:
def scroll_oled():
    while True:
        bluePin.duty(300) #blue
        greenPin.duty(50) #red
        oled.fill(1) # setting the background of the oled display
        for i in range (-50,128, +2): # to make the text move from right to left on the oled display        
            oled.text((message), i,15,0)
            oled.show()
            sleep(0.02)
            oled.fill(1) # we clear the display each time after showing a message          
        oled.show() # we call the predefined function for displaying the text on oled display
        oled.fill(1) #clearing the dislpay


start_new_thread(recmensaje, []) # we start the thread with the function that receives messages from the server (has to be first)
scroll_oled() # order of this is very important !

