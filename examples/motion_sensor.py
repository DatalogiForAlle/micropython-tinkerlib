import machine
import tinkerlib

tinkerlib.initialize()
motion_sensor = tinkerlib.LSM9DS1(machine.Pin(17), machine.Pin(16))
#buzzer = tinkerlib.Buzzer(machine.Pin(27))

def main():
    pitch = motion_sensor.pitch
    roll = motion_sensor.roll
    yaw = motion_sensor.yaw
    print(pitch, roll, yaw)

    #if 25 < pitch < 80 and 50 < roll < 140:
    #    print("buzz")
    #    buzzer.tone(2637, 100)

tinkerlib.repeat(main, 10)
tinkerlib.run()
