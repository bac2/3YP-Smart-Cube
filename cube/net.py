import time
import requests
import logging
import hmac
import hashlib
from log import Log 
from cube import Rotation

POST_URL = 'http://ubuntu.lan:8080'

class Network:

	def __init__(self, cube):
		self.log = Log()
		self.cube_code = cube.code
		self.secret_code = cube.secret_code
	
	#Hash data of the form {'time':datetime, 'rotation':rotation}
	def send_rotation_data(self, rotation):
		try:
			hmac_obj = hmac.new(str(self.secret_code), str(rotation.get_rotation())+str(rotation.get_time()), hashlib.sha224)
			digest = hmac_obj.hexdigest()
			post_data = {'rotation':rotation.get_rotation(), 'time':rotation.get_time(), 'digest':digest}
			url = POST_URL + "/update/" + self.cube_code
			response = requests.post(url, params=post_data)
			print response.content

			self.check_log()
		except IOError as  e:
			print e

			#We have a problem. Write it to the log file!
			self.log.write_to_log(rotation)
	
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
	
