import machine
import time
import tinkerlib

# Connections:
#  - G to GND (Ground)
#  - V to 3V3 (3.3V)
#  - S to pin 16

led = tinkerlib.LED(machine.Pin(16, machine.Pin.OUT))

for i in range(10):
    led.on()
    print("on")
    time.sleep(1)
    print("off")
    led.off()
    time.sleep(1)
