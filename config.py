from micropython import const
import ujson as json

# Callback timers - it's silly but I like to keep these prime so that in theory they don't 'beat' with each other
CONTROLLER_LOOP_MS: int = const(211) # first prime above 200
TEMP_LOOKUP_MS: int = const(1009) # First prime above 20000

# Configurable values
#
try:
    with open("config.json", "r") as f:
        saved_config = json.load(f)
        WIFI_SSID: str = saved_config["WIFI_SSID"]
        WIFI_PASS: str = saved_config["WIFI_PASS"]
except Exception as e:
    print("Failed to load config file, no wifi will be available", e)
