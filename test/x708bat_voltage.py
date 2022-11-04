#!/usr/bin/python3

import struct
import smbus as smbus
import sys

bus = smbus.SMBus(1) # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
address = 0x36
read = bus.read_word_data(address, 2)
swapped = struct.unpack("<H", struct.pack(">H", read))[0]
print(round(swapped * 1.25 /1000/16,2))

