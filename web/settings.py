#!/usr/bin/python

# This file controls displaying and updating the user settings

from base_handler import BaseHandler
from data_objects import User, Profile, Cube
import tornado.web

#Displays the settings page
class SettingsHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.params['profiles'] = self.get_profiles()
		self.params['cubes'] = self.get_cubes()
		self.params['user'] = self.get_current_user()
		self.params['events'] = []
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

#Deals with editing a profile
class ProfileEditHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self, pid):
		name = self.get_argument("name")
		desc = self.get_argument("desc")
		s1 = self.get_argument("s1")
		s2 = self.get_argument("s2")
		s3 = self.get_argument("s3")
		s4 = self.get_argument("s4")
		s5 = self.get_argument("s5")
		s6 = self.get_argument("s6")
		current_user = self.get_current_user()
		
		self.db.execute("UPDATE Profile SET name=%s, describe_line=%s, side1=%s, side2=%s, side3=%s, side4=%s, side5=%s, side6=%s WHERE creator_id=%s AND id=%s;", name, desc, s1, s2, s3, s4, s5, s6, current_user.user_id, pid)
		self.write("success")

#Deals with deleting a profile
class ProfileDeleteHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self, pid):
		from MySQLdb import IntegrityError
		current_user = self.get_current_user()
		
		try:
			self.db.execute("DELETE FROM Profile WHERE id=%s AND creator_id=%s;", pid, current_user.user_id)
			self.write("success")
		except IntegrityError:
			#Foreign key constraint failed - Transitions exist
			self.write("profile in use")

#Deals with creating a profile
class ProfileCreateHandler(BaseHandler):
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

#Deals with changing the profile of a cube
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

