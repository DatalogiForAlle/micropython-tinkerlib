import machine
import tinkerlib

# Connections:
#  - G to GND (Ground)
#  - V to 3V3 (3.3V)
#  - S to pin 18

def on_button_down():
    print("Down")

def on_button_up():
    print("Up")

pin18 = machine.Pin(18, mode=machine.Pin.IN)

tinkerlib.initialize()
button = tinkerlib.Button(pin18,
                          button_down=on_button_down,
                          button_up=on_button_up)
tinkerlib.run()
