import machine
import time
import tinkerlib

# Example code for Potentiometer
pin32 = machine.Pin(32, mode=machine.Pin.IN)
pot = tinkerlib.Potentiometer(pin32)

for i in range(100):
    print(pot.read())
    time.sleep_ms(200)
