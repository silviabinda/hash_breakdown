/* 

SPDX-FileCopyrightText: © 2024 Silvia Binda Heiserova silviaheiserova@gmail.com

SPDX-License-Identifier: MIT

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::: Hash Breakdown by Silvia Binda Heiserova, 2024 :::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::: CODE EXECUTED FROM ESP32 (TFT Display "small") :::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

ESP32 details: 
Device Name: esp32-9FFE8C
MAC Address: 24-DC-C3-9F-FE-8C
Reserved IP Address: 192.168.0.103

TFT display details:
Resolution: 800 x 480 pixel
Driver: SSD1963
bought from: https://techfun.sk/produkt/nedotykovy-5-displej-800x480/

******************************************************************************************************************************
This code is executed on ESP32, which is physically connected to the TFT 800x480px display.
Connection to GPIOs:
CS -> GPIO33
RS/DC -> GPIO15
RST -> GPIO32
WR -> GPIO4
RD -> GPIO2
LED_A -> 3.3V
3.3V -> 3V3
GND -> GND
db0 -> GPIO12
db1 -> GPIO13
db2 -> GPIO26
db3 -> GPIO18
db4 -> GPIO17
db5 -> GPIO16
db6 -> GPIO27
db7 -> GPIO14

!!! NEVER USE GPIO25 WHEN WORKING WITH WIFI ON ESP32 !!!

The code does 2 basic tasks: 

1) Receiving messages (variable called "message") from PC (Raspberry Pi 4) via UDP communication. 
      //for this UDP communication we use an offline router, which is connected via Wifi to this ESP32 and via LAN cable to PC
      //we have previously set a stable IP address on the router for PC and for this ESP32
              
2) Displaying the received messages on the TFT display
      
******************************************************************************************************************************
*/

//libraries for controlling the TFT display
#include "SPI.h"
#include "TFT_eSPI.h"

//include this font
#include "NotoSansMonoSCB20.h"
#include "Final_Frontier_28.h"
#include "Latin_Hiragana_24.h"
#include "NotoSansBold36.h"

//library for wifi connection to our offline router for udp communication:
#include <WiFi.h>

//library for udp communication:
#include <WiFiUdp.h>

//#include "Free_Fonts.h" // Include the free fonts library Free_Fonts.h if needed (copy it to the same folder as this code)

// The font names are arrays references, thus must NOT be in quotes ""
#define AA_FONT_HEADER NotoSansMonoSCB20
#define AA_FONT_TEXT Final_Frontier_28
#define AA_FONT_LATIN Latin_Hiragana_24
#define AA_FONT_RECT NotoSansBold36

int rectWidth = 400; // Width of the rectangle
int rectHeight = 200; // Height of the rectangle

//int rectX = (tft.width() - rectWidth) / 2; // X-coordinate of the top-left corner of the rectangle
//int rectY = (tft.height()) / 2 + 40; // Y-coordinate of the top-left corner of the rectangle


// Use hardware SPI
TFT_eSPI tft = TFT_eSPI();
TFT_eSprite spr = TFT_eSprite(&tft); // Sprite class needs to be invoked

unsigned long drawTime = 0;

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


void setup(void) {
  // initializing Wifi connection to offline router and udp messages receiving
  Serial.begin(9600);
  initWiFi();
  udp.begin(udpPort);
  Serial.print("start"); 
  Serial.print(tft.height());
  Serial.print(tft.width());

  // initializing and initial setting of the tft dislpay:
  tft.begin();
  tft.setRotation(1); //horizontal

  spr.setColorDepth(16); // 16-bit colour needed to show antialiased fonts
}

void loop() {

  //tft.fillScreen(TFT_BLACK);

  int xpos = tft.width();
  int ypos = tft.height();

  char message[500]; //set a limit of the characters of the message
  memset(message, 0, 500);
  //processing incoming packet, must be called before reading the buffer:
  udp.parsePacket();
  //receive response from server:
  if(udp.read(message, 500) > 0)
  //!! problem ze mi vzdy posuva riadok dolu
  //skus set cursor radu od gpt
  {
  //tft.loadFont(AA_FONT_HEADER);
    tft.loadFont(AA_FONT_LATIN);
    tft.fillScreen(TFT_BLACK);
    tft.fillRect(0, 0, 800, 60, TFT_GREEN); //(x, y, width, height, color);
    tft.fillRect(5, 5, 790, 50, TFT_BLACK);
    //tft.fillRect(0, 61, 800, 180, TFT_BLACK);
    tft.setCursor(8, 0); //Set fixed values for the cursor so the text appears on the same place always
    //tft.setTextFont(4);
    //tft.setTextFont(&NotoSansBold36);
    tft.setTextWrap(true); // Wrap on width
    tft.setTextColor(TFT_YELLOW); //or CYAN
    // //tft.drawString("1234567", 240, 160, 7);
    tft.println();
    //tft.print("  *** This is the definition of feminism I found in the world wide web: ***");
    //tft.print("  THIS IS THE DEFINITION OF FEMINISM I FOUND IN THE WORDL WIDE WEB:");
    tft.print("                            *** H A S H  B R E A K D O W N ***");
    tft.println();
    tft.println();
    tft.print("    ");
    tft.setTextColor(TFT_WHITE);
    tft.loadFont(AA_FONT_TEXT);
    tft.print(message);

    delay(10000);
    blinkText();

  }

  // ??? Dalsiu spravu (final hash) ako vytlacit ? //if(udp.read(message, 500) == 64))
  // }

}

void blinkText() {
  tft.loadFont(AA_FONT_RECT);
  tft.setTextColor(TFT_BLACK);
  tft.fillRect(190, 300, 410, 100, TFT_CYAN);
  tft.fillRect(210, 325, 380, 70, TFT_GREEN);
  bool magentaColor = true; // Initial color state
  if (magentaColor) {
    tft.fillRect(210, 325, 380, 70, TFT_MAGENTA);
  } else {
    tft.fillRect(205, 305, 390, 90, TFT_GREEN);
  }
  magentaColor = !magentaColor; // Toggle the color state
  tft.drawString("hashing in progress", 210, 330, 4); // Font 4 for fast drawing with background
  
}

#ifndef LOAD_GLCD
//ERROR_Please_enable_LOAD_GLCD_in_User_Setup
#endif

#ifndef LOAD_FONT2
//ERROR_Please_enable_LOAD_FONT2_in_User_Setup!
#endif

#ifndef LOAD_FONT4
//ERROR_Please_enable_LOAD_FONT4_in_User_Setup!
#endif

#ifndef LOAD_FONT6
//ERROR_Please_enable_LOAD_FONT6_in_User_Setup!
#endif

#ifndef LOAD_FONT7
//ERROR_Please_enable_LOAD_FONT7_in_User_Setup!
#endif

#ifndef LOAD_FONT8
ERROR_Please_enable_LOAD_FONT8_in_User_Setup!
#endif

#ifndef LOAD_GFXFF
ERROR_Please_enable_LOAD_GFXFF_in_User_Setup!
#endif

/*
  This code is using parts of the example that draws fonts (as used by the Adafruit_GFX library) onto the
  screen. These fonts are called the GFX Free Fonts (GFXFF) in this library.

  Other True Type fonts could be converted using the utility within the
  "fontconvert" folder inside the library. This converted has also been
  copied from the Adafruit_GFX library.

  Since these fonts are a recent addition Adafruit do not have a tutorial
  available yet on how to use the utility.   Linux users will no doubt
  figure it out!  In the meantime there are 48 font files to use in sizes
  from 9 point to 24 point, and in normal, bold, and italic or oblique
  styles.

  This example sketch uses both the print class and drawString() functions
  to plot text to the screen.

  Make sure LOAD_GFXFF is defined in the User_Setup.h file within the
  TFT_eSPI library folder.

  --------------------------- NOTE ----------------------------------------
  The free font encoding format does not lend itself easily to plotting
  the background without flicker. For values that changes on screen it is
  better to use Fonts 1- 8 which are encoded specifically for rapid
  drawing with background.
  -------------------------------------------------------------------------
  
  >>>>>>>>>>>>>>>>>>>>>>>>>>> WARNING <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

  As supplied with the default settings the sketch has 11 fonts loaded,
  i.e. GLCD (Font 1), Font 2, Font 4, Font 6, Font 7, Font 8 and five Free Fonts,
  even though they are not all used in the sketch.
  
  Disable fonts you do not need in User_Setup.h in the library folder.

  #########################################################################
  ###### DON'T FORGET TO UPDATE THE User_Setup.h FILE IN THE LIBRARY ######
  #########################################################################
*/
