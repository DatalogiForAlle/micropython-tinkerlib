import machine
import machine
import time
from tinkerlib import Potentiometer

# Example code for Potentiometer
pot = Potentiometer(machine.Pin(32, mode=machine.Pin.IN))
for i in range(100):
    print(pot.value())
    time.sleep_ms(200)
