import machine
import time
from tinkerlib import ADKeypad

def on_button_down(x):
    print(x)

adkey = ADKeypad(machine.Pin(32, mode=machine.Pin.IN),
                 button_down=on_button_down)
