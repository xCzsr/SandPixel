# SPI - Functional test on MAX7219 with 7 segment display
# Import necessary functions
# spi lib
# https://forum-raspberrypi.de/forum/thread/39007-techniker-projekt-12-gro%C3%9Fe-7-segment-anzeigen-an-raspi-multiplexen
# max7219 datasheet
# https://datasheets.maximintegrated.com/en/ds/MAX7219-MAX7221.pdf
import time
import spidev
# Transfer project to a name (here spi)
spi = spidev.SpiDev()
# "put the MAX7219 in the track" must be made after each power lot of the MAX7219
spi.open(0, 0)  # Enable SPI interface CS0, Chanel 0
# SPI clock runs at a maximum of 50kHz, is absolutely necessary (MAX7219 according to data sheet max 10MHz)
spi.max_speed_hz = 50000
spi.writebytes([0x0F, 0x01])  # display test on,
time.sleep(0.5)  # 0.5s
spi.writebytes([0x0F, 0x00])  # Display test off
spi.writebytes([0x0C, 0x01])  # Normal mode
spi.writebytes([0x0A, 0x0F])  # intensity maximum
# spi.writebytes ([0x0B, 0x07]) # Scanlimit show all
spi.close()  # SPI interface in sleep mode (end of serialization MAX7219)
# in direct control mode
spi.open(0, 0)  # Enable SPI interface CS0, Chanel 0
# SPI clock runs at a maximum of 50kHz, is absolutely necessary (MAX7219 according to data sheet max 10MHz)
spi.max_speed_hz = 50000
spi.writebytes([0x09, 0x00])  # Enable direct mode

IMAGES = [
    (
        0b10000000,
        0b11000000,
        0b11100000,
        0b11111111,
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000
    ), (
        0b10000000,
        0b11000000,
        0b11100000,
        0b01111111,
        0b10000000,
        0b00000000,
        0b00000000,
        0b00000000
    ), (
        0b10000000,
        0b11000000,
        0b11100000,
        0b00111111,
        0b01000000,
        0b10000000,
        0b00000000,
        0b00000000
    ), (
        0b10000000,
        0b11000000,
        0b11100000,
        0b00011111,
        0b00100000,
        0b01000000,
        0b10000000,
        0b00000000
    ), (
        0b10000000,
        0b11000000,
        0b11100000,
        0b00001111,
        0b00010000,
        0b00100000,
        0b01000000,
        0b10000000
    ), (
        0b10000000,
        0b11000000,
        0b01100000,
        0b10000111,
        0b00001000,
        0b00010000,
        0b00100000,
        0b11000000
    ), (
        0b10000000,
        0b11000000,
        0b00100000,
        0b01000011,
        0b10000100,
        0b00001000,
        0b00010000,
        0b11100000
    ), (
        0b10000000,
        0b01000000,
        0b10000000,
        0b00100001,
        0b01000010,
        0b10000100,
        0b00001000,
        0b11110000
    ), (
        0b00000000,
        0b10000000,
        0b01000000,
        0b10000000,
        0b00100001,
        0b01000010,
        0b10000100,
        0b11111000
    ), (
        0b00000000,
        0b00000000,
        0b10000000,
        0b01000000,
        0b10000000,
        0b00100001,
        0b11000010,
        0b11111100
    ), (
        0b00000000,
        0b00000000,
        0b00000000,
        0b10000000,
        0b01000000,
        0b10000000,
        0b11100001,
        0b11111110
    ), (
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b10000000,
        0b11000000,
        0b11100000,
        0b11111111,
    )]

# spi.writebytes ([0x'Digit number ', 0b'Bit pattern segments'])
y = 0.20  # sleep variable
try:
    while(1):
        for x in range(len(IMAGES)):
            spi.writebytes([0x01, IMAGES[x][0]])  # Digit 1 = 1
            time.sleep(y)
            spi.writebytes([0x02, IMAGES[x][1]])  # Digit 2 = 2
            time.sleep(y)
            spi.writebytes([0x03, IMAGES[x][2]])  # Digit 3 = 3
            time.sleep(y)
            spi.writebytes([0x04, IMAGES[x][3]])  # Digit 4 = 4
            time.sleep(y)
            spi.writebytes([0x05, IMAGES[x][4]])  # Digit 5 ​​= 5
            time.sleep(y)
            spi.writebytes([0x06, IMAGES[x][5]])  # Digit 6 = 6
            time.sleep(y)
            spi.writebytes([0x07, IMAGES[x][6]])  # Digit 7 = 7
            time.sleep(y)
            spi.writebytes([0x08, IMAGES[x][7]])  # Digit 8 = 8
            time.sleep(y)


except KeyboardInterrupt:
    spi.writebytes([0x01, 0])  # Digit 1 = 1
    time.sleep(y)
    spi.writebytes([0x02, 0])  # Digit 2 = 2
    time.sleep(y)
    spi.writebytes([0x03, 0])  # Digit 3 = 3
    time.sleep(y)
    spi.writebytes([0x04, 0])  # Digit 4 = 4
    time.sleep(y)
    spi.writebytes([0x05, 0])  # Digit 5 ​​= 5
    time.sleep(y)
    spi.writebytes([0x06, 0])  # Digit 6 = 6
    time.sleep(y)
    spi.writebytes([0x07, 0])  # Digit 7 = 7
    time.sleep(y)
    spi.writebytes([0x08, 0])  # Digit 8 = 8
    time.sleep(y)
    spi.close()
