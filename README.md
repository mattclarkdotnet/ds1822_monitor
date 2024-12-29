# Monitor a set of DS18xx one-wire thermometers

This is a micropython app to monitor a set of DS18xx one-wire thermometers and run a webserver to get the outputs.

The thermometers are issued a temperature read instruction once per second, and the temperatures are also read out once per second.

The server presents the results at http://ds18.local/temps

## Dev Setup

```sh
uv pip install -U micropython-rp2-pico_w-stubs --target typings
```
