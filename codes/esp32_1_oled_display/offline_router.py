import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

while not wlan.isconnected():
    try:
        print("Trying to connect to the network...")
        wlan.connect("SSID", "password")
        while not wlan.isconnected():
            pass  # Wait here until connected
        print("Connected successfully.")
        print(wlan.ifconfig())
    except Exception as e:
        print("An error occurred: ", str(e))
        print("Retrying in 10 seconds...")
        #time.sleep(10)  # Wait for 10 seconds before retrying
else:
    print("WiFi connection details:")
    print(wlan.ifconfig())