#!/bin/sh
echo none >/sys/class/leds/led0/trigger
python /home/pi/3YP/cube/leds.py
echo none [mmc0] >/sys/class/leds/led0/trigger
