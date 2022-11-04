#!/usr/bin/env python
import RPi.GPIO as GPIO
import json
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN)

stringPowerLoss = 'AC Power Loss OR Power Adapter Failure'
stringPowerOK   = 'AC Power OK,Power Adapter OK'

dPLD = {
  'status': 3, # 3 - initial state, 1 - Power Loss, 2 - Power OK
  'description':  stringPowerLoss
}

def handlePower():
    nStatus = GPIO.input(6)

    if dPLD['status'] != nStatus: 
        if nStatus: # if port 6 = 1
           dPLD['status'] = nStatus
           dPLD['description'] = stringPowerLoss
        else:       # if port 6 != 1
           dPLD['description'] = stringPowerOK
           dPLD['status'] = 2

        jsonString = json.dumps(dPLD)
        jsonFile = open('/usr/share/hassio/homeassistant/files/ac_power.json','w')
        jsonFile.write(jsonString)
        jsonFile.close()

def my_callback(channel):
    handlePower()

GPIO.add_event_detect(6, GPIO.BOTH, callback=my_callback)

handlePower()

print("Power Loss Detection Started...")
while True:
  time.sleep(5)

print("Power Loss Detection Finished...")
