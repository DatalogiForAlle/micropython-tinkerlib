import time
import machine
import lsm9ds1
import tinkerlib

lsm = lsm9ds1.LSM9DS1(machine.I2C(-1, machine.Pin(17), machine.Pin(16)))


# For devices without magnetometer
filter = tinkerlib.ComplimentaryFilter()
while True:
   pitch, roll, yaw = filter.process(10, lsm.read_accel(), lsm.read_gyro())
   print((pitch, roll))
   time.sleep_ms(10)


# For devices with magnetometer
# filter = tinkerlib.ComplimentaryFilter(has_magnetometer=True)
# while True:
#    pitch, roll, yaw = filter.process(10, lsm.read_accel(),
#                                      lsm.read_gyro(),
#                                      lsm.read_magnet())
#    print((pitch, roll))
#    time.sleep_ms(10)
