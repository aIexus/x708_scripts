#!/usr/bin/env python
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN)

if GPIO.input(6):     # if port 6 == 1
  print ("---AC Power Loss OR Power Adapter Failure---")
else:                  # if port 6 != 1
  print ("---AC Power OK,Power Adapter OK---")

