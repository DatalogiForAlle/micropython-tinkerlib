import machine
import math
import neopixel
import time
from tinkerlib.base import repeat, schedule
import tinkerlib.contrib.lsm9ds1
from tinkerlib.contrib.fusion import Fusion

class Potentiometer():
    """ ESP32: ports 32-39, ESP8266: ADC(0)"""
    def __init__(self, pin):
        self.pin = pin
        self.adc = machine.ADC(self.pin)
        self.adc.width(machine.ADC.WIDTH_10BIT)
        self.adc.atten(machine.ADC.ATTN_11DB)

    def read(self):
        return self.adc.read()


class Microphone():
    """ ESP32: ports 32-39, ESP8266: ADC(0)"""
    def __init__(self, pin):
        self.pin = pin
        self.adc = machine.ADC(self.pin)
        self.adc.width(machine.ADC.WIDTH_10BIT)
        self.adc.atten(machine.ADC.ATTN_11DB)

    def read(self):
        """Returns amplitude in voltage 0-5V"""
        startMillis = time.ticks_ms()
        peakToPeak = 0
        signalMax = 0
        signalMin = 1024

        while time.ticks_ms() - startMillis < sampleWindow:
            sample = self.adc.read()
            if sample < 1024:
                signalMax = max(signalMax, sample)
                signalMin = min(signalMin, sample)
        peakToPeak = signalMax - signalMin
        volts = (peakToPeak * 5.0) / 1024.0
        return volts


class DustSensor():
    """ """
    def __init__(self, pin, sampletime_ms=30000):
        self.pin = pin
        self.sampletime_ms = sampletime_ms

    # Waits for the pin to turn LOW/HIGH, depending on the value argument
    # and measures how long time it has that value.
    def _pulseInTimeout(self, pin, value, endTime):
        # Wait till we hit the wanted value
        while pin.value() != value:
            if(time.ticks_ms() > endTime):
                return 0
        # Start timing
        start = time.ticks_us()
        # Wait till we are no longer == value (or time passes)
        while pin.value() == value and time.ticks_ms() < endTime:
            pass
        now = time.ticks_us()
        tdiff = time.ticks_diff(now, start)
        return tdiff

    def read(self):
        starttime_ms = time.ticks_ms()
        endTime = starttime_ms + self.sampletime_ms
        lowpulseoccupancy_us = 0
        while time.ticks_ms() < endTime:
            duration_us = self._pulseInTimeout(self.pin, 0, endTime)
            lowpulseoccupancy_us = lowpulseoccupancy_us+duration_us
        # Integer percentage 0%-100%
        ratio = lowpulseoccupancy_us/(self.sampletime_ms*10.0)
        # Using spec sheet curve
        concentration = 1.1*pow(ratio, 3)-3.8*pow(ratio, 2)+520*ratio+0.62
        return concentration


class PIRSensor():
    update_frequency = 10 # 10 Hz
    """Passive InfraRed (PIR) sensor - detects motion"""
    def __init__(self, pin, callback):
        self.pin = pin
        self.callback = callback
        self.pin.irq(handler=self.on_rising,
                     trigger=machine.Pin.IRQ_RISING)
        self.rising_flag = False
        repeat(self.check_rising, frequency=PIRSensor.update_frequency)

    def check_rising(self):
        if self.rising_flag:
            self.rising_flag = False
            self.callback()

    def on_rising(self, pin):
        self.rising_flag = True

    def value(self):
        return self.pin.value()


class Button():
    update_frequency = 10 # 10 Hz

    """TinkerKit Crash Sensor / button"""
    def __init__(self, pin, button_down, button_up=None):
        self.pin = pin
        self.pin.init(pull=machine.Pin.PULL_UP)
        self.button_down = button_down
        self.button_up = button_up
        self.state = self.pin.value()
        self.pin.irq(handler=self.on_change,
                     trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING)
        self.button_change_flag = False
        repeat(self.button_check, frequency=Button.update_frequency)

    def button_check(self):
        if self.button_change_flag:
            self.button_change_flag = False
            new_state = self.pin.value()
            if self.state == 0 and new_state == 1:
                if self.button_up:
                    self.button_up()
            elif self.state == 1 and new_state == 0:
                self.button_down()
            self.state = new_state

    def on_change(self, pin):
        self.button_change_flag = True


class ADKeypad():
    update_frequency = 60 # 60 Hz
    """5 button keypad"""
    def __init__(self, pin, button_down=None, button_up=None):
        self.pin = pin
        self.adc = machine.ADC(self.pin)
        self.adc.width(machine.ADC.WIDTH_10BIT)
        self.adc.atten(machine.ADC.ATTN_11DB)
        self.button_down = button_down
        self.button_up = button_up
        self.button_last_state = self.button_state()
        repeat(self.button_check, frequency=ADKeypad.update_frequency)

    def voltage_to_key(self, v):
        thresholds = [4, 20, 70, 150, 600]
        for i in range(len(thresholds)):
            if v < thresholds[i]:
                return i
        return None

    def button_state(self):
        return self.voltage_to_key(self.adc.read())

    def button_check(self):
        new_state = self.button_state()
        if self.button_last_state != new_state:
            if new_state is None:
                if self.button_up:
                    self.button_up()
            else:
                if self.button_down:
                    self.button_down(new_state)
        self.button_last_state = new_state

class LED:
    def __init__(self, pin):
        self.pin = pin
        # Mode function not available on ESP boards
        # self.pin.mode(machine.Pin.OUT)

    def on(self):
        self.pin.value(1)

    def off(self):
        self.pin.value(0)

class Buzzer:
    def __init__(self, pin, dutycycle_in_percent=False):
        self.pin = pin
        self.pwm = machine.PWM(self.pin, freq=0, duty=0)
        self.noTone()
        self.dutycycle_in_percent=dutycycle_in_percent

    def enable(self, frequency, dutycycle=50):
        if frequency != 0:
            self.pwm.init()
            self.pwm.freq(frequency)
            if self.dutycycle_in_percent:
                self.pwm.duty(dutycycle)
            else:
                self.pwm.duty(int(1023*dutycycle/100))

    def tone(self, frequency, duration=None, dutycycle=50):
        def task():
            self.enable(frequency, dutycycle)
        schedule(task)
        if duration != None:
            schedule(self.noTone, delay=duration)
            # time.sleep_ms(duration)
            # self.pwm.deinit()

    def noTone(self):
        self.pwm.deinit()

## Servo class from https://bitbucket.org/thesheep/micropython-servo/
## MIT Licensed, written by Radomir Dopieralski
class Servo:
    """
    A simple class for controlling hobby servos.

    Args:
        pin (machine.Pin): The pin where servo is connected. Must support PWM.
        freq (int): The frequency of the signal, in hertz.
        min_us (int): The minimum signal length supported by the servo.
        max_us (int): The maximum signal length supported by the servo.
        angle (int): The angle between the minimum and maximum positions.

    """
    def __init__(self, pin, freq=50, min_us=600, max_us=2400, angle=180):
        self.min_us = min_us
        self.max_us = max_us
        self.us = 0
        self.freq = freq
        self.angle = angle
        self.pwm = machine.PWM(pin, freq=freq, duty=0)

    def write_us(self, us):
        """Set the signal to be ``us`` microseconds long. Zero disables it."""
        if us == 0:
            self.pwm.duty(0)
            return
        us = min(self.max_us, max(self.min_us, us))
        duty = us * 1024 * self.freq // 1000000
        self.pwm.duty(duty)

    def write_angle(self, degrees=None, radians=None):
        """Move to the specified angle in ``degrees`` or ``radians``."""
        if degrees is None:
            degrees = math.degrees(radians)
        degrees = degrees % 360
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * degrees // self.angle
        self.write_us(us)


class LEDStrip(neopixel.NeoPixel):
    def __init__(self, pin, n, bpp=3, timing=1):
        neopixel.NeoPixel.__init__(self, pin, n, bpp, timing)

    def __len__(self):
        return self.n

    def __str__(self):
        return str([self[i] for i in range(self.n)])

    def fillN(self, color, n):
        for i in range(n):
            self[i] = color
        self.write()

    def clear(self):
        self.fillN((0, 0, 0), len(self))

class LSM9DS1:
    update_frequency = 10
    def __init__(self, scl, sda):
        self.i2c = machine.I2C(-1, scl, sda)
        self.lsm = tinkerlib.contrib.lsm9ds1.LSM9DS1(self.i2c)
        self.filter = Fusion()
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        repeat(self.update, frequency=LSM9DS1.update_frequency)

    def update(self):
        self.accel = self.lsm.read_accel()
        self.gyro = self.lsm.read_gyro()
        self.magnet = self.lsm.read_magnet()
        self.filter.update(self.accel, self.gyro, self.magnet)
        self.pitch = self.filter.pitch
        self.roll = self.filter.roll
        self.yaw = self.filter.heading
