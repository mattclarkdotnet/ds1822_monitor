import micropython
from machine import Timer, Pin
from utime import ticks_ms, ticks_diff
from gc import mem_free
import ds18x20
import onewire

from config import CONTROLLER_LOOP_MS, TEMP_LOOKUP_MS


class TemperatureInput:
    def __init__(self) -> None:
        self._ready = False
        self._timer = Timer()
        try:
            ow = onewire.OneWire(Pin(12))  # create a OneWire bus on GPIO12
            self._ds = ds18x20.DS18X20(ow)
            self._roms: list = self._ds.scan()
            print("ds18x20 roms:", self._roms)
            if len(self._roms) > 0:
                print("Found DS devices: ", self._roms)
                self.temps = [0.0] * len(self._roms)
                self._ready = True
            else:
                raise Exception("No DS devices found")
        except Exception as e:
            print("Error setting up temperature sensor")
            print(e)
            self._ds = None
            self._roms = []
            self.temps = []

    def read_temps(self, _):
        if not self._ready:
            print("Temperature sensor not ready")
            return
        for i, rom in enumerate(self._roms):
            self.temps[i] = self._ds.read_temp(rom)
            print("Temp:", i, self.temps[i])

    def run(self):
        self._timer.init(
            period=TEMP_LOOKUP_MS, mode=Timer.PERIODIC, callback=self._irq_handler
        )

    def stop(self):
        self._timer.deinit()

    @micropython.native
    def _irq_handler(self, _):
        if not self._ready:
            return
        self._ds.convert_temp()
        micropython.schedule(self.read_temps, None)


class Controller:
    def __init__(self) -> None:
        self.start_time = ticks_ms()
        self.temperature_input = TemperatureInput()
        self.timer = Timer()

    def run(self):
        self.temperature_input.run()
        self.timer.init(
            period=CONTROLLER_LOOP_MS, mode=Timer.PERIODIC, callback=self._irq_handler
        )

    def stop(self):
        self.timer.deinit()
        self.temperature_input.stop()

    def _irq_handler(self, _):
        micropython.schedule(self.eventloop, None)

    def eventloop(self, _):
        pass

    def json_status(self) -> dict:
        try:
            temps = dict(enumerate(self.temperature_input.temps))
            status = {
                "temps C": temps,
                "free kB": mem_free(),
                "uptime S": ticks_diff(ticks_ms(), self.start_time) // 1000,
            }
            print("Status:", status)
            return status
        except Exception as e:
            print("Error in json_status")
            print(e)
            return {"error": str(e)}
