from base_handler import BaseHandler

import tornado.auth
import tornado.web


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
