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

def infrequent():
    print("The quick brown fox jumps over the lazy dog")

tinkerlib.initialize()
tinkerlib.repeat(main, 1)   # 1 Hz
tinkerlib.repeat(toggle_led, 20) # 20 Hz (20 toggles, 10 blinks per second)
tinkerlib.repeat_every(infrequent, 60) # every 60 seconds (every minute)
tinkerlib.run()
