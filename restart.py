import os
from time import sleep
from pythonwifi.iwlibs import Wireless

WIFI_NAME = "B-LINK_B058F0"
INTERFACE_NAME = "wlan0"
SLEEP_TIME = 0.25

last = WIFI_NAME
wifi = Wireless(INTERFACE_NAME);

while True:
    current = wifi.getEssid()
    if (current != last and current == WIFI_NAME):
        os.system("sudo service uv4l_raspicam restart")
    last = current
    sleep(SLEEP_TIME)