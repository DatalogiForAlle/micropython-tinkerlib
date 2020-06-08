import machine
import tinkerlib

# Connections:
#  - G to GND (Ground)
#  - V to 3V3 (3.3V)
#  - S to pin 18

# Example code PIR sensor / motion detector
def onDetection():
    print("Hello world!")

tinkerlib.initialize()
pir = tinkerlib.PIRSensor(machine.Pin(18, mode=machine.Pin.IN),
                          callback=onDetection)
tinkerlib.run()
