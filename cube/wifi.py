import urllib2
import urllib
import time
from log import Log 
from cube import Rotation

class Network:

	def __init__(self):
		self.log = Log()
	
	#Hash data of the form {'time':datetime, 'rotation':rotation}
	def send_rotation_data(self, rotation):
		try:
			post_data = {'rotation':rotation.get_rotation(), 'time':rotation.get_time()}
			post_encode = urllib.urlencode(post_data)
			request = urllib2.Request("http://users.ecs.soton.ac.uk/bac2g10/cube.php", post_encode)
			response = urllib2.urlopen(request)
			print response.read()

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
	
