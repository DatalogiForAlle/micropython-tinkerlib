import machine
import time
from tinkerlib import PIRSensor

# Example code PIR sensor / motion detector
def on_detection():
    print("Hello world!")

pir = PIRSensor(machine.Pin(16, mode=machine.Pin.IN),
                callback=on_detection)
