from wifi import Network
import time
from cube import Cube, Rotation
import argparse
import threading
from bottle import run, route, template
import signal
import logging
import sys

#Programs main method...
parser = argparse.ArgumentParser()
parser.add_argument("action", help="start/test")
args = parser.parse_args()


class RunThread( threading.Thread ):
	def start(self):
		self.daemon = True

	def run (self):
		print "Run Thread started."

		net = Network()
		prev_rotation = -1
		while(1):
			cube.check_rotation()
			current_rotation = cube.get_rotation()
			if(current_rotation != prev_rotation):
				#Send it to the server
				logging.info('Rotation changed from ', prev_rotation, ' to ', current_rotation)
				rot = Rotation(current_rotation, time.time())
				net.send_rotation_data(rot)
			prev_rotation = current_rotation
			time.sleep(10)
@route('/')
def getRot():
	cube.check_rotation()
	current_rot = cube.get_rotation()
	pos = {1:'UP',2:'DOWN',3:'LEFT',4:'RIGHT',5:'FRONT',6:'BACK'}
	return template('Hello! Current upwards is {{rot}}', rot=pos[current_rot])

if(args.action == 'start'):
	#Do some stuff...
	logging.basicConfig(filename="cube.log")
			
	cube = Cube()
	RunThread().start()
	run(host='0.0.0.0', port=8080)


