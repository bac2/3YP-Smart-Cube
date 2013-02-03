#encoding: utf-8
import os

import logging
import datetime
import tornado.httpserver
import tornado.ioloop
import tornado.auth
import tornado.web
import tornado.options
import torndb

from tornado.options import define, options

define("port", default=8080, help="Run on the given port", type=int)
define("mysql_user", default='cube', help='User to connect to database with')
define("mysql_password", default='cubism_rules&£', help="Password to connect to mysql")
define("mysql_host", default='localhost', help='Host to connect to')
define("mysql_database", default='3yp', help='The database to use')

logging.basicConfig(filename='web.log', level=logging.INFO)

class User():
	def __init__(self,user_info):
		self.name = user_info['name']
		self.email = user_info['email']
		self.user_id = user_info['id']
	
	def __str__(self):
		return {'name':self.name, 'email':self.email, 'user_id':self.user_id}

class App(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", HomeHandler),
			(r"/login", GoogleHandler),
			(r"/logout", LogoutHandler),
			(r"/friends", FriendsHandler),
			(r"/update", UpdateHandler),
			(r"/register/([A-Z0-9a-z]{6})", RegisterHandler),
			(r"/register", RegisterHandler)
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
	
	def initialize(self):
		self.params = {}
		current_user = self.get_current_user()
		if current_user == None:
			self.params['loggedin'] = False
		else:
			self.params['loggedin'] = True
			self.params['fname'] = current_user.name.split(" ")[0]
	
	@property
	def db(self):
		return self.application.db

	def get_current_user(self):
		user_id = self.get_secure_cookie('user')
		if not user_id:
			return None
		user_info = self.db.get('SELECT * FROM User WHERE id=%s', user_id)
		return User(user_info)

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
		self.render("friends.html", **self.params)

	def get_friends(self):
		#Get users and wrap them in objects
		current_user = self.get_current_user()
		friends = self.db.query("SELECT * FROM User WHERE id IN (SELECT user2 FROM Friend WHERE user1=%s)", current_user.user_id)
		users = []
		for friend in friends:
			#Make a friend object out of the information for each friend
			users.append(User(friend))
		print [ i.name for i in users]
		return users

class UpdateHandler(BaseHandler):
	
	#Receives an update from a cube
	def post(self):
		import hmac
		rotation = self.get_argument("rotation")
		time = self.get_argument("time")
		cube_id = self.get_argument("cube_id")
		digest = self.get_argument("digest")
		#Get the cube key from the database
		cube_info = self.db.get("SELECT secret_key, owner FROM Cube WHERE id=%s", cube_id)
		hmac = hmac.new(cube_info['secret_key'], rotation+time, hashlib.sha1)
		our_digest = hmac.digest()
	
		if our_digest != digest:
			return #Ignore it, it isn't from a cube we know!

		#Do some stuff here
		print rotation, time, cube_info['owner']

class RegisterHandler(BaseHandler):
	
	#Registers a cube to a user after scanning the QR code
	@tornado.web.authenticated
	def get(self, unique_code):
		cube = self.db.get("SELECT * FROM Cube WHERE unique_id=%s", unique_code)
		if cube:
			self.params['registered'] = True
		else:
			self.params['registered'] = False
			self.params['unique_code'] = unique_code
		self.render('register.html', **self.params)

	def post(self):
		current_user = self.get_current_user()
		self.db.execute("INSERT INTO Cube (Owner, unique_id) VALUES (%s, %s);", current_user.user_id, self.get_argument('unique_code')) 
		self.params['complete'] = True
		self.render('register.html', **self.params)

	

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(App())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if(__name__ == '__main__'):
	main()
