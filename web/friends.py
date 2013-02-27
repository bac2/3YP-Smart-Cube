from base_handler import BaseHandler
from data_objects import User, Profile, Cube

import tornado.web

class FriendsHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):	
		#Get friends from the database
		self.params['friends'] = self.get_friends()
		self.params['cubes'] = self.get_cubes()
		self.render("friends.html", **self.params)

	def get_friends(self):
		#Get users and wrap them in objects
		current_user = self.get_current_user()
		friends = self.db.query("SELECT * FROM User WHERE id IN (SELECT user2 FROM Friend WHERE user1=%s)", current_user.user_id)
		users = []
		for friend in friends:
			#Make a friend object out of the information for each friend
			current = User(friend)
			current.cubes = self.get_cubes(current)
			users.append(current)
		return users


class FindFriendsHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.write("hello!")

