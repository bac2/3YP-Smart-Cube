import os

import logging
import datetime
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.auth
import torndb

from tornado.options import define, options
from data_objects import User, Profile, Cube

define("port", default=8080, help="Run on the given port", type=int)
define("mysql_user", default='cube', help='User to connect to database with')
define("mysql_password", default='cubism_rules', help="Password to connect to mysql")
define("mysql_host", default='localhost', help='Host to connect to')
define("mysql_database", default='3yp', help='The database to use')

logging.basicConfig(filename='web.log', level=logging.INFO)


class App(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", HomeHandler),
			(r"/login", GoogleHandler),
			(r"/logout", LogoutHandler),
			(r"/friends", FriendsHandler),
			(r"/update/([A-Za-z0-9]{6})", UpdateHandler),
			(r"/register/([A-Z0-9a-z]{6})", RegisterHandler),
			(r"/register", RegisterHandler),
			(r"/settings", SettingsHandler),
			(r"/settings/profile", ProfileUpdateHandler),
			(r"/settings/cube", CubeUpdateHandler),
			(r"/about", AboutHandler)
			]
		settings = dict(
			app_title=u'Smart-Cube',
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			#xsrf_cookies=True,
			cookie_secret=u"secret123&3%sdn5A",
			login_url="/login",
			debug=True
			)
		tornado.web.Application.__init__(self, handlers, **settings) 

		#Set up global DB connection here
		self.db = torndb.Connection(
			host=options.mysql_host, database=options.mysql_database,
			user=options.mysql_user, password=options.mysql_password)


#All handlers inherit this. Defines useful things
class BaseHandler(tornado.web.RequestHandler):
	
	#Sets up the params hash
	def initialize(self):
		self.params = {}
		current_user = self.get_current_user()
		if current_user == None:
			self.params['loggedin'] = False
		else:
			self.params['loggedin'] = True
			self.params['fname'] = current_user.name.split(" ")[0]
	
	#Shortcut to the db
	@property
	def db(self):
		return self.application.db

	#Returns the current user as an object
	def get_current_user(self):
		user_id = self.get_secure_cookie('user')
		if not user_id:
			return None
		user_info = self.db.get('SELECT * FROM User WHERE id=%s', user_id)
		return User(user_info)

	#Returns all the cubes for the current user
	def get_cubes(self):
		current_user = self.get_current_user()
		#gets info about the cube and the profile id when it was last updated
		cubes_info = self.db.query("SELECT Cube.id, owner, unique_id, position, time as last_transition, (SELECT profile_id FROM Profile INNER JOIN ProfileTransition ON ProfileTransition.profile_id = Profile.id WHERE last_transition > time ORDER BY time DESC LIMIT 1) as corresponding_profile FROM Cube INNER JOIN (SELECT cube_id, position, time FROM Transition ORDER BY time DESC) as alias ON cube_id = Cube.id WHERE owner=%s GROUP BY Cube.id;", current_user.user_id);

		cubes = []
		for cube_info in cubes_info:
			current = Cube(cube_info)
			#Fills in the currently selected profile information
			#This could be different from the active profile on the last transition
			profile_info = self.db.get("SELECT Profile.id as id, describe_line, name, creator_id, side1, side2, side3, side4, side5, side6, profile_id, time, cube_id FROM Profile INNER JOIN ProfileTransition ON ProfileTransition.profile_id = Profile.id WHERE cube_id = %s ORDER BY time DESC LIMIT 1;", current.cube_id)
			if profile_info is None:
				current.profile = None
			else:
				current.profile = Profile(profile_info)
		
			#Fills in the active profile at the time of last transition
			if cube_info['corresponding_profile'] is None:
				current.corresponding_profile = None
			else:
				profile_info = self.db.get("SELECT * FROM Profile WHERE id=%s;", cube_info['corresponding_profile'])
				current.corresponding_profile = Profile(profile_info)
			current.owner = current_user
			cubes.append(current)
		return cubes

class HomeHandler(BaseHandler):
	def get(self):
		self.render('index.html', **self.params)

class GoogleHandler(BaseHandler, tornado.auth.GoogleMixin):
	@tornado.web.asynchronous
	def get(self):
		#Pass off to Google to do the login
		if self.get_argument("openid.mode", None):
			self.get_authenticated_user(self._on_auth)
			return
		self.authenticate_redirect()

	def _on_auth(self, user):
		if not user:
			tornado.web.HTTPError(500, "Google Authentication Failure")
			return

		#Create or get user from the database
		user_info = self.db.get("SELECT * FROM User WHERE email=%s", user["email"])
		if not user_info:
			#This user doesn't exist yet - Add them
			user_id = self.db.execute("INSERT INTO User (Name, Email) VALUES (%s, %s);", user['name'], user['email'])
		else:
			#Otherwise, grab their ID
			user_id = user_info['id']
		
		#Set a logged in Cookie
		self.set_secure_cookie("user", str(user_id))
		self.redirect(self.get_argument("next", "/"))

class LogoutHandler(BaseHandler):
	def get(self):
		self.clear_cookie("user")
		self.redirect("/")

class FriendsHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):	
		#Get friends from the database
		friends = self.get_friends()
		self.params['friends'] = friends
		self.params['cubes'] = self.get_cubes()
		self.render("friends.html", **self.params)

	def get_friends(self):
		#Get users and wrap them in objects
		current_user = self.get_current_user()
		friends = self.db.query("SELECT * FROM User WHERE id IN (SELECT user2 FROM Friend WHERE user1=%s)", current_user.user_id)
		users = []
		for friend in friends:
			#Make a friend object out of the information for each friend
			users.append(User(friend))
		return users


class UpdateHandler(BaseHandler):
	
	#Receives an update from a cube
	def post(self, unique_code):
		import hmac
		import hashlib
		rotation = self.get_argument("rotation")
		time = self.get_argument("time")
		digest = self.get_argument("digest")
		#Get the cube key from the database
		cube_info = self.db.get("SELECT id, secret_key, owner FROM Cube WHERE unique_id=%s", unique_code)
		if not cube_info:
			#We don't know about this cube
			self.write("Unknown cube code")
			return
		hmac_obj = hmac.new(str(cube_info['secret_key']), str(rotation)+str(time), hashlib.sha224)
		our_digest = hmac_obj.hexdigest()
	
		if our_digest != digest:
			print "Digests don't match:", our_digest, digest
			return #Ignore it, it isn't from a cube we know!

		#Do some stuff here - Add a rotation to the database
		self.db.execute("INSERT INTO Transition (position, time, cube_id) VALUES (%s, %s, %s);", rotation, time, cube_info['id'])
		

class RegisterHandler(BaseHandler):
	
	#Registers a cube to a user after scanning the QR code
	@tornado.web.authenticated
	def get(self, unique_code):
		cube = self.db.get("SELECT * FROM Cube WHERE unique_id=%s", unique_code)
		self.params['complete'] = False
		if cube:
			self.params['registered'] = True
		else:
			self.params['registered'] = False
			self.params['unique_code'] = unique_code
		self.render('register.html', **self.params)

	def post(self):
		import hashlib
		current_user = self.get_current_user()
		secret_code = hashlib.sha224(self.get_argument('unique_code')).hexdigest()
		self.db.execute("INSERT INTO Cube (secret_key, Owner, unique_id) VALUES (%s, %s, %s);", secret_code, current_user.user_id, self.get_argument('unique_code')) 
		self.params['complete'] = True
		self.render('register.html', **self.params)

class SettingsHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.params['profiles'] = self.get_profiles()
		self.params['cubes'] = self.get_cubes()
		self.render('settings.html', **self.params)

	def get_profiles(self):
		current_user = self.get_current_user()
		profiles_info = self.db.query("SELECT * FROM Profile WHERE creator_id = %s", current_user.user_id)
		#Convert to objects
		profiles = []
		for profile_info in profiles_info:
			profile = Profile(profile_info)
			profile.creator = current_user
			profiles.append(profile)
		return profiles

class ProfileUpdateHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
		name = self.get_argument("name")
		desc = self.get_argument("desc")
		s1 = self.get_argument("s1")
		s2 = self.get_argument("s2")
		s3 = self.get_argument("s3")
		s4 = self.get_argument("s4")
		s5 = self.get_argument("s5")
		s6 = self.get_argument("s6")
		current_user = self.get_current_user()
		
		self.db.execute("INSERT INTO Profile (creator_id, name, describe_line, side1, side2, side3, side4, side5, side6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);", current_user.user_id, name, desc, s1, s2, s3, s4, s5, s6) 
		self.redirect("/settings")	

class CubeUpdateHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
		profile_id = self.get_argument("pid")
		cube_id = self.get_argument("cid")
		
		profile_name = self.save_profile(cube_id, profile_id)
		
		self.write(profile_name)

	def save_profile(self, cube_id, profile_id):

		self.db.execute("INSERT INTO ProfileTransition (cube_id, profile_id, time) VALUES (%s, %s, NOW());", cube_id, profile_id)

		profile = self.db.get("SELECT * FROM Profile WHERE id = %s", profile_id)
		return profile['name']

class AboutHandler(BaseHandler):
	def get(self):
		self.render("about.html", **self.params)

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(App())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
	main()

