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

class App(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", HomeHandler),
			(r"/login", GoogleHandler)
			]
		settings = dict(
			app_title=u'Smart-Cube',
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			xsrf_cookies=True,
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
	@property
	def db(self):
		return self.application.db

class HomeHandler(BaseHandler):
	def get(self):
		self.render("index.html")

class GoogleHandler(BaseHandler, tornado.auth.GoogleMixin):
	@tornado.web.asynchronous
	def get(self):
		if self.get_argument("openid.mode", None):
			self.get_authenticated_user(self._on_auth)
			return
		self.authenticate_redirect()

	def _on_auth(self, user):
		if not user:
			tornado.web.HTTPError(500, "Google Authentication Failure")
			return
		print "Login Success from", user['name']
		self.redirect(self.get_argument("next", "/"))
		#Do some stuff here....

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(App())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

#@app.route('/<user>/<time>/<rotation>', method='PUT')
#def update_rotation(user, time, rotation):
#	datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
#	s = "Rotation to " + rotation + " at " + time + " from user " + user;
#	logging.info(s)
#	return s

if(__name__ == '__main__'):
	main()



