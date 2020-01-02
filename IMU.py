#!/usr/bin/python
# Ceasar Navarro
# SDA = PIN 3 = GPIO 2
# SCL = PIN 5 = GPIO 3
import smbus
import math
import time

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c


def read_byte(reg):
    return bus.read_byte_data(address, reg)


def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value


def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


def dist(a, b):
    return math.sqrt((a*a)+(b*b))


def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


bus = smbus.SMBus(1)  # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect

bus.write_byte_data(address, power_mgmt_1, 0)


def main():
    while(1):
        try:
            # true value of Gyroscope
            gyro_xout = read_word_2c(0x43)
            gyro_yout = read_word_2c(0x45)
            gyro_zout = read_word_2c(0x47)
            # scaled value of Gyroscope
            gyro_xout_scaled = (gyro_xout / 131)
            gyro_yout_scaled = (gyro_yout / 131)
            gyro_zout_scaled = (gyro_zout / 131)
            # true value of Accelerometer
            accel_xout = read_word_2c(0x3b)
            accel_yout = read_word_2c(0x3d)
            accel_zout = read_word_2c(0x3f)
            # Scaled value of Accelerometer
            accel_xout_scaled = accel_xout / 16384.0
            accel_yout_scaled = accel_yout / 16384.0
            accel_zout_scaled = accel_zout / 16384.0

            print("gyro_xout: ", ("%5d" % gyro_xout),
                  " Scaled: ", str(gyro_xout_scaled))
            print("gyro_yout: ", ("%5d" % gyro_yout),
                  " Scaled: ", str(gyro_yout_scaled))
            print("gyro_zout: ", ("%5d" % gyro_zout),
                  " Scaled: ", str(gyro_zout_scaled))
            print("\n")
            print("Accel_xout: ", ("%6d" % accel_xout),
                  " Scaled: ", str(accel_xout_scaled))
            print("Accel_yout: ", ("%6d" % accel_yout),
                  " Scaled: ", str(accel_yout_scaled))
            print("Accel_zout: ", ("%6d" % accel_zout),
                  " Scaled: ", str(accel_zout_scaled))
            print("\n")
            print("X Rotation: ", get_x_rotation(
                accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
            print("Y Rotation: ", get_y_rotation(
                accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
            print("\n")
            time.sleep(.75)

        except KeyboardInterrupt:
            return 0


if __name__ == "__main__":
    main()
