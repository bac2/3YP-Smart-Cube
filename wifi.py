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
	i = 0
	while True:
		i +=1
		if not is_wifi_on():
			print 'WiFi Off - Cycling'
			os.system('sudo /home/pi/3YP/cycle_wifi.sh')
		else:
			#Wifi is on
			if i % 60 == 0:
				i = 0
				os.system('sudo service ntp stop')
				os.system('sudo ntpd -qg')
		time.sleep(60)

