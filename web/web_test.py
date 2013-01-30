from bottle import Bottle, route, template
import logging
import datetime

app = Bottle();
logging.basicConfig(filename='web.log', level=logging.INFO)

@app.route('/')
def index():
	return 'Welcome to the Smart-Cube site!'

@app.route('/<user>/<time>/<rotation>', method='PUT')
def update_rotation(user, time, rotation):
	datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
	s = "Rotation to " + rotation + " at " + time + " from user " + user;
	logging.info(s)
	return s


app.run(host='0.0.0.0', port='8080')


