import machine
import tinkerlib

# Connections:
#  - Yellow wire to VUSB (5V)
#  - Green wire to GND (Ground)
#  - Black wire to pin 26 (digital in)

pin26 = machine.Pin(26, machine.Pin.IN)

###### EXAMPLE 1: Default sampletime ######

# Use default sampletime (30 seconds)
dustsensor = tinkerlib.DustSensor(pin26)

# This loop will thus run for 10 * 30 seconds (5 minutes)
for i in range(10):
    concentration = dustsensor.read()
    print(concentration)

###### EXAMPLE 2: Change sampletime ######

# Use a sampletime of 15 seconds
dustsensor = tinkerlib.DustSensor(pin26, sampletime_ms=15000)

# This loop will run for 10 * 15 seconds (2 minute, 30 seconds)
for i in range(10):
    concentration = dustsensor.read()
    print(concentration)
