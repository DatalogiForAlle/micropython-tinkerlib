import machine
import tinkerlib

# Connections:
#  - G to GND (Ground)
#  - V to 3V3 (3.3V)
#  - S to pin 32 (only works on pin 32, 33, 36, 37, 38, 39)

def on_button_down(key):
    print(key)

pin32 = machine.Pin(32, mode=machine.Pin.IN)
tinkerlib.initialize()
adkey = tinkerlib.ADKeypad(pin32, button_down=on_button_down)
tinkerlib.run()
