import time
import machine
import lsm9ds1
import tinkerlib

lsm = lsm9ds1.LSM9DS1(machine.I2C(-1, machine.Pin(17), machine.Pin(16)))
filter = ComplimentaryFilter()

while True:
   pitch, roll = filter.process(10, lsm.read_accel(), lsm.read_gyro())
   print((pitch, roll))
   time.sleep_ms(10)
