#!/usr/bin/python
from net import Network
from cube import Cube, Rotation
from bottle import run, route, template
from multiprocessing import Process, Lock
import datetime
import time
import argparse
import logging
import sys

#Programs main method...
parser = argparse.ArgumentParser()
parser.add_argument("action", help="start/test")
args = parser.parse_args()
l = Lock()


def check_loop(l):
	net = Network(cube)
	prev_rotation = -1
	while(True):
		try:
			l.acquire()
			cube.check_rotation()
			current_rotation = cube.get_rotation()
			l.release()
			if(current_rotation != prev_rotation):
				#Send it to the server
				logging.info('Rotation changed from ', prev_rotation, ' to ', current_rotation)
				rot = Rotation(current_rotation, datetime.datetime.now())
				net.send_rotation_data(rot)
			prev_rotation = current_rotation
			time.sleep(10)
		except StandardError, e:
			print e
			logging.error("Generic Error! " + str(e))

@route('/')
def getRot():
	l.acquire()
	cube.check_rotation()
	current_rot = cube.get_rotation()
	l.release()
	pos = {1:'UP',2:'DOWN',3:'LEFT',4:'RIGHT',5:'FRONT',6:'BACK'}
	return template('Hello! Current upwards is {{rot}}', rot=pos[current_rot])

def event_checker(l):
	#Runs to check for events to flash the led
	from events import EventChecker
	l.acquire()
	net = Network(cube)
	l.release()

	ec = EventChecker(net)
	while True:
		ec.check_events()
		time.sleep(60)

if(args.action == 'start'):
	#Do some stuff...
#	sys.stdout = open("/home/pi/3YP/cube/output.log", "w+")
	logging.basicConfig(filename="/home/pi/3YP/cube/cube.log")
	logging.info("Started cube running")
		
	cube = Cube()
	p = Process(target=check_loop, args=(l,))
	p.start()
	p2 = Process(target=event_checker, args=(l,))
	p2.start()
	run(host='0.0.0.0', port=8080)


