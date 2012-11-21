import wifi
import time

class Log:
	def __init__(self):
		self.logfile = open('cubeData.log', 'ra')
		data = self.logfile.read();
	
	def send(self, currentRotation):
		if(wifi.is_wifi_on()):
			#We have a connection...
			print "Wifi is connected"
			wifi.send_post_data({'rotation':currentRotation, 'time':time.time()})
		else:
			print "Wifi not connected"
		
log = Log()
log.send(3)
		
