import requests
import hashlib
import hmac
import json
import time
from os import system
import signal


API_KEY = 'Of7yGQET1k41KbB-mmJv'
CUBE_CODE = '460'
URL = 'http://bubuntu-vm.lan:8080'

class MusicController:

    def __init__(self):
        self.state = 'stopped'

    def play(self):
        system("rhythmbox-client --play &")
	print "Playing..."
        self.state = 'playing'

    def stop(self):
        system("rhythmbox-client --stop &")
	print "Stopped..."
        self.state = 'stopped'

    def pause(self):
        system("rhythmbox-client --pause & ")
	print "Paused..."
        self.state = 'paused'

class Cube:

    def __init__(self):
        self.music = MusicController()
	self.last_pos = -1
        self.actions = {}
        self.actions[0] = self.music.pause
        self.actions[1] = self.music.play
	self.actions[2] = self.music.pause
	self.actions[3] = self.music.play
	self.actions[4] = self.music.pause
	self.actions[5] = self.music.play

    def check_state(self):
        server = URL
        url = '/cube'
        thetime = time.time()
        url = url+'?time='+str(thetime)+'&user=1'

        auth_key = self.get_auth(url)
        response = requests.get(server+url+'&api='+auth_key)
        try:
            response = json.loads(response.content)
        except StandardError:
            print 'Error: Incorrect auth details. Is your API key correct?'
            return

        if response != []:
            for cube in response:
                if cube['code'] == CUBE_CODE:
                    #We want the position
                    pos = int(cube['position'])
		    if pos != self.last_pos:
                        self.actions[pos-1]()
			self.last_pos = pos


    def get_auth(self, url):
        hmac_obj = hmac.new(API_KEY, url, hashlib.sha256)
        return hmac_obj.hexdigest()

def handler(signum, frame):
	system('rhythmbox-client --quit')
	exit(0)
        
if __name__ == '__main__':
    system('rhythmbox-client &')
    time.sleep(3)
    signal.signal(signal.SIGINT, handler)
    cube = Cube()
    while(True):
    	cube.check_state()
	time.sleep(2)
    system('rhythmbox-client --quit')

