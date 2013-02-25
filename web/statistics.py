from base_handler import BaseHandler
from data_objects import Cube, Profile, User
import tornado.web

class StatsHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.params['cubes'] = self.get_cubes()
		
		self.render("stats.html", **self.params)
	
