#!/usr/bin/env python
# Ceasar Navarro

import re
import time
import argparse
import max7219.led as led


from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop

if __name__ == "__main__":

    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=1)
    light = led.matrix()
    counter = 0
    try:
        while(counter < 2):
            #demo(args.cascaded, args.block_orientation, args.rotate)

            light.pixel(0, 0, 1)
            time.sleep(1)
            light.pixel(0, 0, 0)
            time.sleep(1)
            light.pixel(1, 1, 1)
            time.sleep(1)
            light.pixel(1, 1, 0)
            counter += 1

    except KeyboardInterrupt:
        pass
