from base_handler import BaseHandler
from data_objects import User, Profile
import tornado.web
import json

class ProfileEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Profile):
            return {'profile_id':obj.profile_id, 'describe_line':obj.describe_line, 'creator_id':obj.creator_id, 'name':obj.name, 'sides':obj.sides}

#Deals with creating a profile and viewing profiles
class ProfileCreateHandler(BaseHandler):
        @tornado.web.authenticated
        def get(self):
            current_user = self.get_current_user()
            profiles_info = self.db.query("SELECT * FROM Profile WHERE creator_id=%s;", current_user.user_id)

            profiles = []
            for profile_info in profiles_info:
                current = Profile(profile_info)
                profiles.append(current)

            self.write(json.dumps(profiles, cls=ProfileEncoder))

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
		
	    profile_id = self.db.execute("INSERT INTO Profile (creator_id, name, describe_line, side1, side2, side3, side4, side5, side6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);", current_user.user_id, name, desc, s1, s2, s3, s4, s5, s6) 
	    self.write(str(profile_id))	

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

