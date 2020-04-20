import machine
import math
import time
import neopixel


class LED:
    def __init__(self, pin):
        self.pin = pin
        # Mode function not available on ESP boards
        # self.pin.mode(machine.Pin.OUT)

    def on(self):
        self.pin.value(1)

    def off(self):
        self.pin.value(0)


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
    """Passive InfraRed (PIR) sensor - detects motion"""
    def __init__(self, pin, callback):
        self.pin = pin
        self.callback = callback
        self.pin.irq(handler=self.on_rising,
                     trigger=machine.Pin.IRQ_RISING)

    def on_rising(self, pin):
        irq_state = machine.disable_irq()
        self.callback()
        machine.enable_irq(irq_state)

    def value(self):
        return self.pin.value()


class Button():
    """TinkerKit Crash Sensor / button"""
    def __init__(self, pin, button_down, button_up=None):
        self.pin = pin
        self.pin.init(pull=machine.Pin.PULL_UP)
        self.button_down = button_down
        self.button_up = button_up
        self.state = self.pin.value()
        self.pin.irq(handler=self.on_change,
                     trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING)

    def on_change(self, pin):
        irq_state = machine.disable_irq()
        new_state = pin.value()
        if self.state == 0 and new_state == 1:
            if self.button_up:
                self.button_up()
        elif self.state == 1 and new_state == 0:
            self.button_down()
        self.state = new_state
        machine.enable_irq(irq_state)


class ADKeypad():
    """5 button keypad"""
    def __init__(self, pin, button_down=None, button_up=None, timer=3):
        self.pin = pin
        self.adc = machine.ADC(self.pin)
        self.adc.width(machine.ADC.WIDTH_10BIT)
        self.adc.atten(machine.ADC.ATTN_11DB)
        self.button_down = button_down
        self.button_up = button_up
        self.button_last_state = self.button_state()
        self.tim = machine.Timer(timer)
        self.tim.init(period=20,
                      mode=machine.Timer.PERIODIC,
                      callback=self.button_check)

    def voltage_to_key(self, v):
        thresholds = [4, 20, 70, 150, 600]
        for i in range(len(thresholds)):
            if v < thresholds[i]:
                return i
        return None

    def button_state(self):
        return self.voltage_to_key(self.adc.read())

    def button_check(self, t):
        new_state = self.button_state()
        if self.button_last_state != new_state:
            if new_state is None:
                if self.button_up:
                    self.button_up()
            else:
                if self.button_down:
                    self.button_down(new_state)
        self.button_last_state = new_state


class Buzzer:
    def __init__(self, pin, dutycycle_in_percent=False):
        self.pin = pin
        self.pwm = machine.PWM(self.pin)
        self.dutycycle_in_percent=dutycycle_in_percent

    def tone(self, frequency, duration=None, dutycycle=50):
        if frequency != 0:
            self.pwm.init()
            self.pwm.freq(frequency)
            if self.dutycycle_in_percent:
                self.pwm.duty(dutycycle)
            else:
                self.pwm.duty(int(1023*dutycycle/100))
        if duration != None:
            time.sleep_ms(duration)
            self.pwm.deinit()

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


GYROSCOPE_SENSITIVITY = 65.536
RADIANS_TO_DEGREES = 57.2958
class ComplimentaryFilter:
    def __init__(self, has_magnetometer=False):
        self.pitch = 0
        self.roll = 0
        self.has_magnetometer = has_magnetometer
        self.weight = 0.02

    def process(self, dt, acceleration, gyro):
        """
        dt: Time since last call to process in milliseconds
        """
        dt = dt / 1000
        acc_x = acceleration[0]
        acc_y = acceleration[1]
        acc_z = acceleration[2]
        gyro_x = gyro[0]
        gyro_y = gyro[1]
        gyro_z = gyro[2]
        w = self.weight
        roll_acc = math.atan2(acc_y, acc_z)*RADIANS_TO_DEGREES
        roll_gyro = (gyro_x / GYROSCOPE_SENSITIVITY) * dt + self.roll
        self.roll = roll_acc * w + (1-w) * roll_gyro
        pitch_acc = math.atan2(acc_x, math.sqrt(pow(acc_y, 2) + pow(acc_z, 2))) * RADIANS_TO_DEGREES
        pitch_gyro = (gyro_y / GYROSCOPE_SENSITIVITY) * dt + self.pitch
        self.pitch = (1-w) * pitch_gyro + w * pitch_acc
        return (self.pitch, self.roll)
