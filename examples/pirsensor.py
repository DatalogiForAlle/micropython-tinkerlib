import machine
import tinkerlib

# Connections:
#  - G to GND (Ground)
#  - V to 3V3 (3.3V)
#  - S to pin 16

# Example code PIR sensor / motion detector
def onDetection():
    print("Hello world!")

pir = tinkerlib.PIRSensor(machine.Pin(16, mode=machine.Pin.IN),
                          callback=onDetection)
