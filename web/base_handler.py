import tornado.web

from data_objects import User, Profile, Cube
#All handlers inherit this. Defines useful things
class BaseHandler(tornado.web.RequestHandler):
	
	#Sets up the params hash
	def initialize(self):
		self.params = {}
		current_user = self.get_current_user()
		if current_user == None:
			self.params['loggedin'] = False
		else:
			self.params['loggedin'] = True
			self.params['fname'] = current_user.name.split(" ")[0]
	
	#Shortcut to the db
	@property
	def db(self):
		return self.application.db

	#Returns the current user as an object
	def get_current_user(self):
		user_id = self.get_secure_cookie('user')
		if not user_id:
			return None
		user_info = self.db.get('SELECT * FROM User WHERE id=%s', user_id)
		return User(user_info)

	#Returns all the cubes for the current user
	def get_cubes(self, user=None, public=False):
		if user is None:
			current_user = self.get_current_user()
		else:
			current_user = user
	
		if public is True:
			cubes_info = self.db.query("SELECT public, Cube.id, owner, unique_id, position, time as last_transition, (SELECT profile_id FROM Profile INNER JOIN ProfileTransition ON ProfileTransition.profile_id = Profile.id WHERE last_transition > time AND cube_id = Cube.id ORDER BY time DESC LIMIT 1) as corresponding_profile FROM Cube LEFT OUTER JOIN (SELECT cube_id, position, time FROM Transition ORDER BY time DESC) as alias ON cube_id = Cube.id WHERE public=TRUE GROUP BY Cube.id;");
		else:
			#gets info about the cube and the profile id when it was last updated
			cubes_info = self.db.query("SELECT Cube.id, public, owner, unique_id, position, time as last_transition, (SELECT profile_id FROM Profile INNER JOIN ProfileTransition ON ProfileTransition.profile_id = Profile.id WHERE last_transition > time AND cube_id = Cube.id ORDER BY time DESC LIMIT 1) as corresponding_profile FROM Cube LEFT OUTER JOIN (SELECT cube_id, position, time FROM Transition ORDER BY time DESC) as alias ON cube_id = Cube.id WHERE owner=%s GROUP BY Cube.id;", current_user.user_id);

		cubes = []
		for cube_info in cubes_info:
			current = Cube(cube_info)
			#Fills in the currently selected profile information
			#This could be different from the active profile on the last transition
			profile_info = self.db.get("SELECT Profile.id as id, describe_line, name, creator_id, side1, side2, side3, side4, side5, side6, profile_id, time, cube_id FROM Profile INNER JOIN ProfileTransition ON ProfileTransition.profile_id = Profile.id WHERE cube_id = %s ORDER BY time DESC LIMIT 1;", current.cube_id)
			if profile_info is not None:
				current.profile = Profile(profile_info)
		
			#Fills in the active profile at the time of last transition
			if cube_info['corresponding_profile'] is not None:
				profile_info = self.db.get("SELECT * FROM Profile WHERE id=%s;", cube_info['corresponding_profile'])
				current.corresponding_profile = Profile(profile_info)
			current.owner = current_user
			cubes.append(current)
		return cubes
		
