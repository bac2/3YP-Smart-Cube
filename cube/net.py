import time
import requests
import logging
import hmac
import hashlib
from log import Log 
from cube import Rotation
from requests.exceptions import ConnectionError

POST_URL = 'http://kanga-bac2g10.ecs.soton.ac.uk'

class Network:

	def __init__(self, cube):
		self.log = Log()
		self.cube_code = cube.code
		self.secret_code = cube.secret_code
	
	#Hash data of the form {'time':datetime, 'rotation':rotation}
	def send_rotation_data(self, rotation):
		try:
			hmac_obj = hmac.new(str(self.secret_code), str(rotation.rotation)+str(rotation.time), hashlib.sha224)
			digest = hmac_obj.hexdigest()
			post_data = {'rotation':rotation.rotation, 'time':rotation.time, 'digest':digest}
			url = POST_URL + "/cube/" + self.cube_code + "/transitions"
			response = requests.post(url, params=post_data)

			self.check_log()
		except ConnectionError as e:
			logging.error("Network Failure:"+ str(e))

			#We have a problem. Write it to the log file!
			self.log.write_to_log(rotation)
	
	#We want to check for any existing logs
	def check_log(self):
		data = self.log.get_backlog()
		if data == False:
			return

		print data

		for rot in data:
			self.send_rotation_data(rot)

	def get_events(self):
		import json
		import hmac
		import hashlib
		url = POST_URL + "/events/"+self.cube_code
		try:
			response = requests.get(url)
		except:
			#If it doesn't work, try again in 60 seconds
			return
		reply = response.content
		events = json.loads(reply)

		accepted_events = []
		for event in events:
			hmac_obj = hmac.new(str(self.secret_code), str(event['action'])+str(event['rotation']), hashlib.sha224)
			digest = hmac_obj.hexdigest()
			if digest == event['digest']:
				accepted_events.append(event)
			else:
				print "Digests dont match: "+digest + " AND "+event['digest']

		return accepted_events
			




if __name__ == '__main__':
	net = Network()
	data = Rotation(time.time(), 3)
	net.send_rotation_data(data)
	data = Rotation(time.time()+1000, 3)
	net.send_rotation_data(data)
	
