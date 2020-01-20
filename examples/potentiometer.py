import machine
import time
import tinkerlib

# Connections:
#  - G to GND (Ground)
#  - V to 3V3 (3.3V)
#  - S to pin 32 (analog input only on pin 32, 33, 36, 37, 38, 39)

# Example code for Potentiometer
pin32 = machine.Pin(32, mode=machine.Pin.IN)
pot = tinkerlib.Potentiometer(pin32)

for i in range(100):
    print(pot.read())
    time.sleep_ms(200)
