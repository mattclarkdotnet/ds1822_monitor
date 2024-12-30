from micropython import alloc_emergency_exception_buf
from gc import threshold
from utime import sleep_ms
from controller import Controller
from tinyweb import webserver
from web import WebController
from wifi import WiFi

# Standard procedure to allow more detail in exception reports from inside IRQ handlers
alloc_emergency_exception_buf(200)
# there are a lot of small allocations in IRQ handlers or their delegates, best to tidy up often instead of waiting for OOM events
# the alternative would be to disable autmatic GC and do it in the main run loop, but that relies on the loop being active
threshold(16384)

print("Sleeping 2 seconds to let hardware settle on controller boot")
sleep_ms(2000)

print("Creating amp controller")
c = Controller()
print("Starting wifi")
wifi = WiFi()
print("Creating webserver")
w = webserver()
print("Setting up webserver")
w.add_resource(WebController(c), "/temps")


def run():
    print("Starting controller")
    c.run()
    print("Starting webserver")
    w.run(host="0.0.0.0", port=80)
    # w.run blocks until shutdown is called
    print("Webserver stopped")


def stop():
    print("Stopping controller")
    c.stop()
    print("Stopping webserver")
    w.shutdown()


if __name__ == "__main__":
    run()
