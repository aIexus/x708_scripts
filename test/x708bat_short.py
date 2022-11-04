#!/usr/bin/env python

import struct
import smbus
import sys

bus = smbus.SMBus(1) # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

address = 0x36
read = bus.read_word_data(address, 2)
swapped = struct.unpack("<H", struct.pack(">H", read))[0]

voltage = swapped * 1.25 /1000/16


address = 0x36
read = bus.read_word_data(address, 4)
swapped = struct.unpack("<H", struct.pack(">H", read))[0]

capacity = swapped/256

print ("******************")
print ("Voltage:%5.2fV" % voltage)
print ("Battery:%5i%%" % capacity)
print ("******************")
