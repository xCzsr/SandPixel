#!/usr/bin/python
# GYRO
# SDA = PIN 3 = GPIO 2
# SCL = PIN 5 = GPIO 3 
# 8x8 Matrix 
# Din = PIN 19 = GPIO 10
# CS = PIN 24 = GPIO 8
# CLK= PIN 23 = GPIO 11

import smbus
import math
import time
import spidev

#spi.writebytes([0x01,IMAGES[x][0]]) # Digit 1 = 1
# Transfer project to a name (here spi)
spi = spidev.SpiDev()
# "put the MAX7219 in the track" must be made after each power lot of the MAX7219
spi.open (0,0) # Enable SPI interface CS0, Chanel 0
spi.max_speed_hz = 50000 # SPI clock runs at a maximum of 50kHz, is absolutely necessary (MAX7219 according to data sheet max 10MHz)
spi.writebytes ([0x0F, 0x01]) # display test on,
time.sleep (0.5) # 0.5s
spi.writebytes ([0x0F, 0x00]) # Display test off
spi.writebytes ([0x0C, 0x01]) # Normal mode 
spi.writebytes ([0x0A, 0x0F]) # intensity maximum 
#spi.writebytes ([0x0B, 0x07]) # Scanlimit show all
spi.close () # SPI interface in sleep mode (end of serialization MAX7219)
# in direct control mode
spi.open (0,0) # Enable SPI interface CS0, Chanel 0
spi.max_speed_hz = 50000 # SPI clock runs at a maximum of 50kHz, is absolutely necessary (MAX7219 according to data sheet max 10MHz)\ 
spi.writebytes ([0x09, 0x00]) # Enable direct mode

#####################################################################################################################################

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
bus.write_byte_data(address, power_mgmt_1, 0)
###############################################################################################################################

def mapp(x,y, in_min, in_max, out_min, out_max):  # Map/interpolation function that maps out the LED 8x8 grid
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min), int((y-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

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
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

# LED MAP 2^n(n = 8 for 8 pixels)
ledMap= [ (128,64,32,16,8,4,2,1),
          (128,64,32,16,8,4,2,1),
          (128,64,32,16,8,4,2,1),
          (128,64,32,16,8,4,2,1),
          (128,64,32,16,8,4,2,1),
          (128,64,32,16,8,4,2,1),
          (128,64,32,16,8,4,2,1),
          (128,64,32,16,8,4,2,1),
        ]

def main():
  z = 0.1
  y = 0.01
  while(1):
      try:
          #true value of Gyroscope
          gyro_xout = read_word_2c(0x43)
          gyro_yout = read_word_2c(0x45)
          gyro_zout = read_word_2c(0x47)
          #scaled value of Gyroscope
          gyro_xout_scaled = (gyro_xout/ 131)
          gyro_yout_scaled = (gyro_yout/ 131)
          gyro_zout_scaled = (gyro_zout/ 131)
          #true value of Accelerometer 
          accel_xout = read_word_2c(0x3b)
          accel_yout = read_word_2c(0x3d)
          accel_zout = read_word_2c(0x3f)
          #Scaled value of Accelerometer 
          accel_xout_scaled = accel_xout / 16384.0
          accel_yout_scaled = accel_yout / 16384.0
          accel_zout_scaled = accel_zout / 16384.0
          rotationX =  get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
          rotationY=  get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
          dotOne = mapp(rotationX,rotationY, -65, 65,0,7)

          # Dot one 
          spi.writebytes([dotOne[0]+1,ledMap[dotOne[0]][dotOne[1]]])
          time.sleep(z)
          spi.writebytes([dotOne[0]+1,0])
          time.sleep(y)

    except KeyboardInterrupt:

        spi.writebytes([0x01,0]) # Digit 1 = 1
        time.sleep(y)
        spi.writebytes([0x02,0]) # Digit 2 = 2
        time.sleep(y)
        spi.writebytes([0x03,0]) # Digit 3 = 3
        time.sleep(y)
        spi.writebytes([0x04,0]) # Digit 4 = 4
        time.sleep(y)
        spi.writebytes([0x05,0]) # Digit 5 ​​= 5
        time.sleep(y)
        spi.writebytes([0x06,0]) # Digit 6 = 6
        time.sleep(y)
        spi.writebytes([0x07,0]) # Digit 7 = 7
        time.sleep(y)
        spi.writebytes([0x08,0]) # Digit 8 = 8
        return 0 

if __name__ == "__main__":
    main()