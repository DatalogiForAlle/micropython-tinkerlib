import machine
import time
from tinkerlib import LED

led = LED(machine.Pin(16, machine.Pin.OUT))

for i in range(10):
    led.on()
    print("on")
    time.sleep(1)
    print("off")
    led.off()
    time.sleep(1)
