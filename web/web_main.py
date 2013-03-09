#!/usr/bin/python

# This file creates the web app and provides links to handlers as well as providing the index/about pages

import os
import logging
import datetime
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import torndb
from tornado.options import define, options

#Our package imports
import auth
import settings
import cube
import profile
import event
import friends
import stats
from base_handler import BaseHandler


class App(tornado.web.Application):
	def __init__(self):
                handlers = [
                        (r"/", HomeHandler),
                        (r"/login", auth.GoogleHandler),
                        (r"/logout", auth.LogoutHandler),
                        (r"/friends", friends.FriendsHandler), #GET, POST
                        (r"/statistics", stats.StatsHandler),
                        (r"/cube/([0-9]+)/profile-transitions", cube.ProfileTransitionHandler), #GET
                        (r"/cube/([0-9]+)/transitions/profile-transition/([0-9]+)", cube.TransitionsHandler), #GET
                        (r"/cube/([0-9]+)/transitions", cube.UpdateHandler), #GET, POST
                        (r"/cube/([0-9]+)/register", cube.RegisterHandler), #GET
                        (r"/cube", cube.RegisterHandler), #POST
                        (r"/settings", settings.SettingsHandler), #GET
                        (r"/profile", profile.ProfileCreateHandler), #POST
                        (r"/profile/([0-9]+)", profile.ProfileEditHandler), #DELETE, POST
                        (r"/cube/([0-9]+)/profile", cube.ProfileHandler), #POST, GET
                        (r"/cube/([0-9]+)/public", cube.PublicHandler), #POST
                        (r"/cube/([0-9]+)/events", cube.EventHandler), #GET, POST
                        (r"/events", event.EventHandler), #GET
                        (r"/events/([0-9]+)", event.EventEditHandler), #POST, DELETE
                        (r"/about", AboutHandler)
                ]

		app_settings = dict(
			app_title=u'Smart-Cube',
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			#xsrf_cookies=True,
			cookie_secret=u"secret123&3%sdn5A",
			login_url="/login",
			debug=True
			)
		tornado.web.Application.__init__(self, handlers, **app_settings) 

		#Set up global DB connection here
		self.db = torndb.Connection(
			host=options.mysql_host, database=options.mysql_database,
			user=options.mysql_user, password=options.mysql_password)

class HomeHandler(BaseHandler):
	def get(self):
		self.params['public_cubes'] = self.get_cubes(public=True)
		self.render('index.html', **self.params)

class AboutHandler(BaseHandler):
	def get(self):
		self.render("about.html", **self.params)

def main():
	define("port", default=8080, help="Run on the given port", type=int)
	define("mysql_user", default='cube', help='User to connect to database with')
	define("mysql_password", default='cubism_rules', help="Password to connect to mysql")
	define("mysql_host", default='localhost', help='Host to connect to')
	define("mysql_database", default='3yp', help='The database to use')

	logging.basicConfig(filename='web.log', level=logging.INFO)

	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(App())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
	main()

