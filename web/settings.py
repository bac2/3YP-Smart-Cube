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
                self.params['apikeys'] = self.get_api_keys()
		self.render('settings.html', **self.params)

        def get_api_keys(self):
            current_user = self.get_current_user()
            keys = self.db.query("SELECT id, api_key, created FROM ApiKey WHERE user_id=%s;", current_user.user_id)
            return keys
                
        def get_events(self):
                current_user = self.get_current_user()
                events_info = self.db.query("SELECT (SELECT name FROM User WHERE id=owner) AS name, (SELECT (CASE rotation WHEN 1 THEN side1 WHEN 2 THEN side2 WHEN 3 THEN side3 WHEN 4 THEN side4 WHEN 5 THEN side5 WHEN 6 THEN side6 end) FROM Profile WHERE id=profile_id) AS side_name, (SELECT unique_id FROM Cube WHERE id=cube_id) AS unique_code, id, action FROM Event WHERE owner = %s", current_user.user_id)
                
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


class ApiKeyHandler(BaseHandler):
        @tornado.web.authenticated
        def post(self):
            import os
            import base64
            key = base64.urlsafe_b64encode(os.urandom(15))
            self.db.execute("INSERT INTO ApiKey (user_id, api_key, created) VALUES (%s, %s, NOW());", self.get_current_user().user_id, key)
            self.write(key)
            return

        @tornado.web.authenticated
        def delete(self, key_id):
            self.db.execute("DELETE FROM ApiKey WHERE id=%s;", key_id)
            self.write("success")
            return
