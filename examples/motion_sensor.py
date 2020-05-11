import time
import machine
import lsm9ds1
import math

i2c = machine.I2C(-1, machine.Pin(17), machine.Pin(16))
print(i2c.scan())

lsm = lsm9ds1.LSM9DS1(machine.I2C(-1, machine.Pin(17), machine.Pin(16)), address_gyro=107, address_magnet=30)


import math
from deltat import DeltaT

#GYROSCOPE_SENSITIVITY = 65.536
GYROSCOPE_SENSITIVITY = 8.75
class ComplementaryFilter:
    def __init__(self, weight=0.5):
        self.pitch = 0
        self.roll = 0
        self.heading = 0
        self.weight = weight
        self.deltat = DeltaT(None)

    def update_nomag(self, acceleration, gyro):
        """
        dt: Time since last call to process in milliseconds
        """
        dt = self.deltat(None)
        #dt = dt / 1000
        acc_x = acceleration[0]
        acc_y = acceleration[1]
        acc_z = acceleration[2]
        gyro_x = gyro[0]
        gyro_y = gyro[1]
        gyro_z = gyro[2]
        w = self.weight

        if acc_x == 0 or acc_y == 0 or acc_z == 0:
            return

        # Complementary filter on roll estimation
        roll_acc = math.degrees(math.atan2(acc_y, acc_z))
        roll_gyro = (gyro_x / GYROSCOPE_SENSITIVITY) * dt + self.roll
        self.roll = roll_acc * w + (1-w) * roll_gyro

        # Complementary filter on pitch estimation
        pitch_acc = math.degrees(math.atan(-1*acc_x/math.sqrt(pow(acc_y,2) + pow(acc_z,2))))
        pitch_gyro = (gyro_y / GYROSCOPE_SENSITIVITY) * dt + self.pitch
        self.pitch = (1-w) * pitch_gyro + w * pitch_acc


    def update(self, acceleration, gyro, magnetometer):
        """
        dt: Time since last call to process in milliseconds
        """
        self.update_nomag(acceleration, gyro)
        self.update_heading3(acceleration, magnetometer)


    def update_heading1(self, acceleration, magnetometer):
        acc_x = acceleration[0]
        acc_y = acceleration[1]
        acc_z = acceleration[2]
        mag_x = magnetometer[0]
        mag_y = magnetometer[1]
        mag_z = magnetometer[2]

        ## TODO currently errors, if l is zero or |magPitch| > 1

        if acc_x == 0 or acc_y == 0 or acc_z == 0:
            return

        # Normalize accelerometer raw values
        l = math.sqrt(pow(acc_x, 2) + pow(acc_y, 2) + pow(acc_z, 2))
        accXnorm = acc_x / l
        accYnorm = acc_y / l

        # Calculate pitch and roll for compensated yaw
        magPitch = math.asin(accXnorm)
        magRoll = -math.asin(accYnorm / math.cos(magPitch))

        # Calculate the new tilt compensated values
        magXcomp = mag_x * math.cos(magPitch) + mag_z * math.sin(magPitch)
        magYcomp = (mag_x * math.sin(magRoll) * math.sin(magPitch)
                    + mag_y * math.cos(magRoll)
                    - mag_z * math.sin(magRoll) * math.cos(magPitch))

        # Calculate tilt compensated heading
        self.heading = math.degrees(math.atan2(magYcomp, magXcomp))
        if self.heading < 0:
            self.heading += 360

    def update_heading2(self, acceleration, magnetometer):
        # from "Applications of Magnetic Sensors for Low Cost Compass Systems" by Michael J. Caruso
        pitch = math.radians(self.pitch)
        roll = math.radians(self.roll)
        x = magnetometer[0]
        y = magnetometer[1]
        z = magnetometer[2]
        Xh = x * math.cos(pitch) + y * math.sin(roll) * math.sin(pitch) - z * math.cos(roll) * math.sin(pitch)
        Yh = y * math.cos(roll) + z * math.sin(roll)
        self.heading = math.degrees(math.atan2(Yh, Xh))
        heading = self.heading
        if self.heading < 0:
            self.heading += 360

        if Xh < 0:
            self.heading = 180 - math.degrees(math.atan2(Yh, Xh))
        elif Xh > 0 and Yh < 0:
            self.heading = - math.degrees(math.atan2(Yh, Xh))
        elif Xh > 0 and Yh > 0:
            self.heading = 360 - math.degrees(math.atan2(Yh, Xh))
        elif Xh == 0.0 and Yh < 0:
            self.heading = 90
        elif Xh == 0.0 and Yh > 0:
            self.heading = 270
        else:
            raise Exception("Not implemented")
        print(Xh, Yh, round(self.heading), round(heading))

    def update_heading3(self, acceleration, magnetometer):
        # From micro:bit
        pitch = math.radians(self.pitch)
        roll = math.radians(self.roll)
        x = magnetometer[0]
        y = magnetometer[1]
        z = magnetometer[2]
        sinPhi = math.sin(roll)
        cosPhi = math.cos(roll)
        sinTheta = math.sin(pitch)
        cosTheta = math.cos(pitch)

        self.heading = math.degrees(math.atan2(x*cosTheta + y*sinTheta*sinPhi + z*sinTheta*cosPhi, z*sinPhi - y*cosPhi))
        if self.heading < 0:
            self.heading += 360
        # perhaps just adjust with 180 degrees?

# For devices without magnetometer
filter = ComplementaryFilter()
while True:
   filter.update(lsm.read_accel(), lsm.read_gyro(), lsm.read_magnet())
   #print((filter.pitch, filter.roll, filter.heading))
   print((filter.heading,))
   time.sleep_ms(10)


# For devices with magnetometer
# filter = tinkerlib.ComplimentaryFilter(has_magnetometer=True)
# while True:
#    pitch, roll, yaw = filter.process(10, lsm.read_accel(),
#                                      lsm.read_gyro(),
#                                      lsm.read_magnet())
#    print((pitch, roll))
#    time.sleep_ms(10)
