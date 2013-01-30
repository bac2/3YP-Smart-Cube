import time
import requests
import logging
from log import Log 
from cube import Rotation

POST_URL = 'http://localhost/'

class Network:

	def __init__(self):
		self.log = Log()
	
	#Hash data of the form {'time':datetime, 'rotation':rotation}
	def send_rotation_data(self, rotation):
		try:
#			post_data = {'rotation':rotation.get_rotation(), 'time':rotation.get_time()}
#			post_encode = urllib.urlencode(post_data)
#			request = urllib2.Request(POST_URL, post_encode)
			url = POST_URL + rotation.get_time() + '/' + rotation.get_rotation()
			response = requests.put(url)
			logging.info('PUT to ' + url)

			self.check_log()
		except:
			#We have a problem. Write it to the log file!
			self.log.write_to_log(data)
	
	#We want to check for any existing logs
	def check_log(self):
		data = self.log.get_backlog()
		if data == False:
			return

		for rot in data:
			self.send_rotation_data(rot)

if __name__ == '__main__':
	net = Network()
	data = Rotation(time.time(), 3)
	net.send_rotation_data(data)
	data = Rotation(time.time()+1000, 3)
	net.send_rotation_data(data)
	
