#!/usr/bin/env python
import struct
import smbus
import sys
import time
import json
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.setwarnings(False)

def readVoltage(bus):
     address = 0x36
     read = bus.read_word_data(address, 2)
     swapped = struct.unpack("<H", struct.pack(">H", read))[0]
     voltage = round(swapped * 1.25 /1000/16,2)
     return voltage

def readCapacity(bus):
     address = 0x36
     read = bus.read_word_data(address, 4)
     swapped = struct.unpack("<H", struct.pack(">H", read))[0]
     capacity = round(swapped/256)
     return capacity

bus = smbus.SMBus(1) # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

dBattery = {
  'voltage': 0,
  'capacity': 0
}

WAIT_TIME = 2          # [s] Sleep interval
BAT_LOW_VOLTAGE = 3.40 # [V] Low Level Battery Voltage value

while True:

 nVoltage = readVoltage(bus)
 nCapacity = readCapacity(bus)

 # If values are changed - save to json file
 if (dBattery['voltage'] != nVoltage or dBattery['capacity'] != nCapacity):
     dBattery['voltage']  = nVoltage
     dBattery['capacity'] = nCapacity
     jsonString = json.dumps(dBattery)
     jsonFile = open('/usr/share/hassio/homeassistant/files/ups_battery.json','w')
     jsonFile.write(jsonString)
     jsonFile.close()

 # If nVoltage is less than BAT_LOW_VOLTAGE - SHUTDOWN
 if nVoltage < BAT_LOW_VOLTAGE:
    print("!!! Battery LOW !!!")
    print("!!! Shutdown in 10 seconds !!!")
    time.sleep(10)
    GPIO.output(13, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(13, GPIO.LOW)

 time.sleep(WAIT_TIME)
