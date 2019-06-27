import machine
import tinkerlib

# Connections:
#  - Yellow wire to VUSB (5V)
#  - Green wire to GND (Ground)
#  - Black wire to pin 26 (digital in)

pin26 = machine.Pin(26, machine.Pin.IN)
dustsensor = tinkerlib.DustSensor(pin26)


# Sampletime defaults to 30 seconds
# This loop will thus run for 10 * 30 seconds (5 minutes)
for i in range(10):
    concentration = dustsensor.read()
    print(concentration)


# Redefine with sampletime set to 10 seconds
dustsensor = tinkerlib.DustSensor(pin26, sampletime_ms=10000)

# This loop will run for 10 * 10 seconds (1 minute, 40 seconds)
for i in range(10):
    concentration = dustsensor.read()
    print(concentration)
