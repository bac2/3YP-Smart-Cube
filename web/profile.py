from base_handler import BaseHandler
from data_objects import User
import tornado.web

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

#Deals with editing/deleting a profile
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

	@tornado.web.authenticated
	def delete(self, pid):
		from MySQLdb import IntegrityError
		current_user = self.get_current_user()
		
		try:
			self.db.execute("DELETE FROM Profile WHERE id=%s AND creator_id=%s;", pid, current_user.user_id)
			self.write("success")
		except IntegrityError:
			#Foreign key constraint failed - Transitions exist
			self.write("profile in use")

