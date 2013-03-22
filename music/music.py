import requests
import hashlib
import hmac
import json
import time
from os import system


API_KEY = 'hello'
CUBE_CODE = '468138'

class MusicController:

    def __init__(self):
        self.state = 'stopped'

    def play(self):
        system("rhythmbox-client --no-start --play")
        self.state = 'playing'

    def stop(self):
        system("rhythmbox-client --stop")
        self.state = 'stopped'

    def pause(self):
        system("rhythmbox-client --pause")
        self.state = 'paused'

class Cube:

    def __init__(self):
        self.music = MusicController()
        self.actions = {}
        self.actions[0] = self.music.pause
        self.actions[1] = self.music.play

    def check_state(self):
        server = 'http://localhost:8080'
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
                    self.actions[pos]()


    def get_auth(self, url):
        hmac_obj = hmac.new(API_KEY, url, hashlib.sha256)
        return hmac_obj.hexdigest()
        
if __name__ == '__main__':
    cube = Cube()
    cube.check_state()

