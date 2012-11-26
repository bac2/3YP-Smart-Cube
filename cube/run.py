from wifi import Network
import time
from cube import Cube, Rotation
import argparse

#Programs main method...
parser = argparse.ArgumentParser()
parser.add_argument("action", help="start/test")
args = parser.parse_args()

if(args.action == 'start'):
	#Do some stuff...
			
	cube = Cube()
	net = Network()
	prev_rotation = -1
	while(1):
		cube.check_rotation()
		current_rotation = cube.get_rotation()
		if(current_rotation != prev_rotation):
			#Send it to the server
			print 'Rotation changed from ', prev_rotation, ' to ', current_rotation
			rot = Rotation(current_rotation, time.time())
			net.send_rotation_data(rot)
		prev_rotation = current_rotation
		time.sleep(10)
else:
	#Run a test script?
