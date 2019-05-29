import machine
import time
from tinkerlib import Button

def on_button_down():
    print("Down")
def on_button_up():
    print("Up")

button = Button(machine.Pin(16, mode=machine.Pin.IN),
                button_down=on_button_down,
                button_up=on_button_up)
