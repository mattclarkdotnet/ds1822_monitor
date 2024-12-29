from micropython import schedule
from machine import Timer
from utime import ticks_ms, ticks_diff
from gc import mem_free
import ds18x20, onewire

from config import CONTROLLER_LOOP_MS, TEMP_LOOKUP_MS

class TemperatureInput:
    def __init__(self) -> None:
        self._timer = Timer()
        ow = onewire.OneWire(Pin(12)) # create a OneWire bus on GPIO12
        self._ds = ds18x20.DS18X20(ow)
        self._roms = self._ds.scan()
        self.temps = [0.0] * len(self._roms)

    def read_temps(self):
        for i, rom in enumerate(self._roms):
            self.temps[i] = self._ds.read_temp(rom)

    def run(self):
        self._timer.init(period=TEMP_LOOKUP_MS, mode=Timer.PERIODIC, callback=self._irq_handler)

    def stop(self):
        self._timer.deinit()

    @micropython.native
    def _irq_handler(self, _):
        self._ds.convert_temp()
        schedule(self.read_temps, None)


class Controller:
    def __init__(self) -> None:
        self.temperature_input = TemperatureInput(adc=hw.temperature)
        self.timer = Timer()


    def run(self):
        self.temperature_input.run()
        self.timer.init(period=CONTROLLER_LOOP_MS, mode=Timer.PERIODIC, callback=self._irq_handler)

    def stop(self):
        self.timer.deinit()
        self.temperature_input.stop()

    def _irq_handler(self, _):
        schedule(self.eventloop, None)

    def eventloop(self, _):
        pass



    def json_status(self) -> dict:
        temps = dict(enumerate(self.temperature_input.temps))
        status = {
            "temps": temps,
            "free": mem_free(),
            "uptime": ticks_diff(ticks_ms(), self.start_time)
        }
        return status
