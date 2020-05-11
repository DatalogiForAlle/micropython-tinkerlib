import machine
import tinkerlib

led = machine.Pin(5, machine.Pin.OUT)
led_state = 0

def toggle_led():
    global led_state
    if led_state == 0:
        led.on()
        print("Blink")
        led_state = 1
    else:
        led.off()
        led_state = 0

def main():
    print("Hello world")

tinkerlib.initialize()
tinkerlib.repeat(main, 1)   # 1 Hz
tinkerlib.repeat(toggle_led, 20) # 20 Hz, 20 LED toggles per second
tinkerlib.run()
