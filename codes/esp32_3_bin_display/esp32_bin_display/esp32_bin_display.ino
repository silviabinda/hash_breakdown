/* 

SPDX-FileCopyrightText: © 2024 Silvia Binda Heiserova silviaheiserova@gmail.com

SPDX-License-Identifier: MIT

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::: Hash Breakdown by Silvia Binda Heiserova, 2024 :::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::: CODE EXECUTED FROM ESP32 (Binary Display) :::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

ESP32 details: 
Device Name: esp32-A045E8
MAC Address: 24-DC-C3-A0-45-E8
Reserved IP Address: 192.168.0.101
******************************************************************************************************************************
This code is executed on ESP32, which is physically connected to DIY Binary Display.
The code does 2 basic tasks: 

1) Receiving a message (variable called "message") from PC (Raspberry Pi 4) via UDP communication. 
      /for this UDP communication we use an offline router, which is connected via Wifi to this ESP32 and via LAN cable to PC
      /we have previously set a stable IP address on the router for PC and for this ESP32
              
2) Displaying the received messages on a DIY Binary Display:
      /we will display the received messages, which in our case is a 0 or a 1
      
******************************************************************************************************************************

________________________________________________________________________________________________________________

The code is run on an ESP32 microcontroller which is connected to the 18 led diodes.
The LED diodes are designed and coded to form a 6 segment numeric display displaying the number 0 or 1.
In each segment, there are 3 LED diodes connected to one pin of the ESP32 WROOM as follows:  

      GPIO23  
        _
GPIO27 | | GPIO22
GPIO26 |_| GPIO19
      GPIO32

NOTE: GPIO25 is interfering with Wifi function of the ESP32 !!!! (Do not use it)

LED diode cathodes (-) are connected to the GND pin on ESP32 via the breadboard with 25 pins.

There is a color pattern applied to the wiring:
Connections from LED diode anodes (+) => red orange wires 
Connections from LED diode cathodes (-) and connection to GND pin of the ESP32 => black color wires
Connection from breadboards size M to respective GPIOs of the ESP32 => violet and orange color wires
________________________________________________________________________________________________________________
*/

//library for wifi connection to our offline router for udp communication:
#include <WiFi.h>

//library for udp communication:
#include <WiFiUdp.h>

//create UDP instance:
WiFiUDP udp;
//set the port number (will be used for receiving messages from PC):
const int udpPort = 8345;

//function for connecting esp32 to Wifi router:
void initWiFi() 
{
  WiFi.mode(WIFI_STA);
  WiFi.begin("SSID", "password"); //ssid and password of offline router
  Serial.println("connecting to wifi ...");
  while (WiFi.status() != WL_CONNECTED) 
  {
    Serial.print('.');
    delay(1000);
  }
  //prints the ip address of esp32 if connected:
  Serial.println(WiFi.localIP());
}

//Define the pins:

int pin_led1 = 23;
int pin_led2 = 22;
int pin_led3 = 19;
int pin_led5 = 27;
int pin_led6 = 26;
int pin_led7 = 32;

//functions for writing numbers on the binary display:
void num_off ()
{
  digitalWrite(pin_led1, LOW);
  digitalWrite(pin_led2, LOW);
  digitalWrite(pin_led3, LOW);
  digitalWrite(pin_led5, LOW);
  digitalWrite(pin_led6, LOW);
  digitalWrite(pin_led7, LOW);
}

void num_zero ()
{
  digitalWrite(pin_led1, HIGH);
  digitalWrite(pin_led2, HIGH);
  digitalWrite(pin_led3, HIGH);
  digitalWrite(pin_led5, HIGH);
  digitalWrite(pin_led6, HIGH);
  digitalWrite(pin_led7, HIGH);
}

void num_one ()
{
  digitalWrite(pin_led1, LOW);
  digitalWrite(pin_led2, HIGH);
  digitalWrite(pin_led3, HIGH);
  digitalWrite(pin_led5, LOW);
  digitalWrite(pin_led6, LOW);
  digitalWrite(pin_led7, LOW);
}


void setup() 
{
  int BUILT_IN_LED = 2; //GPIO of the built in led on ESP32
  //to turn off the built in LED on the ESP32:
  pinMode(BUILT_IN_LED, OUTPUT);
  digitalWrite(BUILT_IN_LED, HIGH);

  pinMode(pin_led1, OUTPUT);
  pinMode(pin_led2, OUTPUT);
  pinMode(pin_led3, OUTPUT);
  pinMode(pin_led5, OUTPUT);
  pinMode(pin_led6, OUTPUT);
  pinMode(pin_led7, OUTPUT);
  Serial.begin(9600);
  initWiFi();
  udp.begin(udpPort);
  Serial.print("start"); 
  // empty display:
  num_off();
}

void loop() 
{
  char message[60]; //set some initial text for the message
  memset(message, 0, 60);
  //processing incoming packet, must be called before reading the buffer:
  udp.parsePacket();
  //receive response from server:
  if(udp.read(message, 60) > 0)
  {
    Serial.print("Sent from main code: ");
    Serial.println((char *)message);
    int message_length = 60;
    if (sizeof(message)<message_length)
    {
      message_length = sizeof(message);
    }
    
    for (int i=0; i<message_length; i++)
    {
      char bit = message[i];

      if (bit == '0') 
      {
        num_zero();
        delay(300);
        num_off();
        delay(200);
      }
      if (bit == '1') 
      {
        num_one();
        delay(200);
        num_off();
        delay(200);
      }
      //else {
      //  num_one();
      //}
 
    }
    //delay(1000);
  }
}
