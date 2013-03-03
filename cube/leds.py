#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(16, GPIO.OUT)

for i in range(0,5):
	GPIO.output(16, GPIO.LOW)
	sleep(0.2)

	GPIO.output(16, GPIO.HIGH)
	sleep(0.2)

	GPIO.output(16, GPIO.LOW)
	sleep(0.2)

	GPIO.output(16, GPIO.HIGH)
	sleep(0.2)

	GPIO.output(16, GPIO.LOW)
	sleep(0.2)

	GPIO.output(16, GPIO.HIGH)
	sleep(0.2)

	GPIO.output(16, GPIO.LOW)
	sleep(2)

	GPIO.output(16, GPIO.HIGH)
	sleep(0.5)





GPIO.cleanup()
