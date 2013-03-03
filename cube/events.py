#!/usr/bin/python
import os

class EventChecker:
	def __init__(self, net):
		#We need the cube
		self.net = net

	def check_events(self):
		events = self.net.get_events()
		if events is None:
			return
		if len(events) > 0:
			os.system("sudo /home/pi/3YP/cube/flashOKled.sh")



if __name__ == '__main__':
	from net import Network
	from cube import Cube
	cube = Cube("420320")
	net = Network(cube)
	ec = EventChecker(net)
	ec.check_events()
