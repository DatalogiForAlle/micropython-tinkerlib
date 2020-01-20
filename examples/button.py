import machine
import tinkerlib

# Connections:
#  - G to GND (Ground)
#  - V to 3V3 (3.3V)
#  - S to pin 16

def onButtonDown():
    print("Down")

def onButtonUp():
    print("Up")

pin16 = machine.Pin(16, mode=machine.Pin.IN)
    
button = tinkerlib.Button(pin16,
                          button_down=onButtonDown,
                          button_up=onButtonUp)
