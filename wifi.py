#!/usr/bin/python
import urllib2
import os
import time

def is_wifi_on():
	try:
		urllib2.urlopen('http://google.com', timeout=1)
		return True
	except:
		return False

if __name__ == '__main__':
	while True:
		if not is_wifi_on():
			print 'WiFi Off - Cycling'
			os.system('sudo /home/pi/3YP/cycle_wifi.sh')
		time.sleep(60)

