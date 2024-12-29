import network
import time

from config import WIFI_SSID, WIFI_PASS

class WiFi:
    def __init__(self):
        network.country("AU")
        network.hostname("ds18.local")
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.config(hostname = "ds18.local")
        self.wlan.active(True)
        self.wlan.connect(WIFI_SSID, WIFI_PASS)
        # Wait for connect or fail
        for attempt in range(1,10):
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            print('waiting for connection, attempt ', attempt, ' status ', self.wlan.status())
            time.sleep(2)

        # Handle connection error
        if self.wlan.status() != 3:
            raise RuntimeError('wifi connection failed, status ', self.wlan.status())
        else:
            print('Connected, IP is ', self.wlan.ifconfig()[0])
