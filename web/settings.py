#!/usr/bin/python

# This file controls displaying and updating the user settings

from base_handler import BaseHandler
from data_objects import User, Profile, Cube, Event
import tornado.web

#Displays the settings page
class SettingsHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.params['profiles'] = self.get_profiles()
		self.params['cubes'] = self.get_cubes()
		self.params['user'] = self.get_current_user()
		self.params['events'] = self.get_events()
		self.render('settings.html', **self.params)
                
        def get_events(self):
                current_user = self.get_current_user()
                events_info = self.db.query("SELECT * FROM Event WHERE owner = %s", current_user.user_id)
                
                events = []
                for event_info in events_info:
                    event = Event(event_info)
                    events.append(event)

                return events

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
class CubeProfileHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self, cube_id, profile_id):
		
		profile_name = self.save_profile(cube_id, profile_id)
		
		self.write(profile_name)

	def save_profile(self, cube_id, profile_id):

		self.db.execute("INSERT INTO ProfileTransition (cube_id, profile_id, time) VALUES (%s, %s, NOW());", cube_id, profile_id)

		profile = self.db.get("SELECT * FROM Profile WHERE id = %s", profile_id)
		return profile['name']

class CubePublicHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self, cube_id, value):
		self.save_public(cube_id, value)
		if value == 1:
			value='Yes'
		else:
			value='No'
		
		self.write(value)

	def save_public(self):
		self.db.execute("UPDATE Cube SET public=%s WHERE id=%s", value, cube_id)


class EventCreateHandler(BaseHandler):
        @tornado.web.authenticated
        def post(self, cube_id):
                side = self.get_argument("side")
                action = self.get_argument("action")
                profile_id = self.get_argument("profile_id")
                current_user = self.get_current_user()

                #First, check the users are friends
                friend = self.db.query("SELECT * FROM Friend WHERE (user1=%s AND user2=(SELECT owner FROM Cube WHERE id=%s)) OR (user1 IN (SELECT owner FROM Cube WHERE id=%s) AND user2=%s);", current_user.user_id, cube_id, current_user.user_id, cube_id);
                if friend is None:
                    #Not friends!
                    return
                
                self.db.execute("INSERT INTO Event (cube_id, owner, action, rotation, profile_id) VALUES (%s, %s, %s, %s, %s);", cube_id, current_user.user_id, action, side, profile_id);

class EventHandler(BaseHandler):
        def get(self, cube_code):
            import json
            import hmac
            import hashlib
            events = self.db.query("SELECT action, rotation, cube_id, (SELECT secret_key FROM Cube WHERE unique_id=%s) AS secret_code FROM Event WHERE owner = (SELECT owner FROM Cube WHERE unique_id=%s) AND action='flashLED' AND rotation = (SELECT position FROM Transition WHERE Transition.cube_id=Event.cube_id ORDER BY time DESC LIMIT 1);", cube_code, cube_code)

            event_list = []
            for event in events:

                hmac_obj = hmac.new(str(event['secret_code']), str(event['action'])+str(event['rotation']), hashlib.sha224)
                digest = hmac_obj.hexdigest()
                del event['secret_code']
                del event['cube_id']
                event['digest'] = digest
                event_list.append(event)

            self.write(json.dumps(event_list))

class EventWebHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        import json
        current_user = self.get_current_user()
        events = self.db.query("SELECT id AS event_id, action, rotation, (SELECT name FROM User WHERE id=(SELECT owner FROM Cube WHERE id=cube_id)) AS name, (SELECT (CASE rotation WHEN 1 THEN side1 WHEN 2 THEN side2 WHEN 3 THEN side3 WHEN 4 THEN side4 WHEN 5 THEN side5 WHEN 6 THEN side6 end) FROM Profile WHERE id=profile_id) AS side_name, cube_id FROM Event WHERE owner = %s AND action='sound' AND rotation = (SELECT position FROM Transition WHERE Transition.cube_id=Event.cube_id ORDER BY time DESC LIMIT 1) AND seen is NULL;", current_user.user_id)

        self.write(json.dumps(events))

    @tornado.web.authenticated
    def post(self, event_id):
        current_user = self.get_current_user()
        self.db.execute("UPDATE Event SET seen=NOW() WHERE id=%s AND owner=%s", event_id, current_user.user_id)


