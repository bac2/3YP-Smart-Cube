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
                    #Try for an API key?
                    user_id = self.get_api_user()
                    if user_id is None:
                        return None

		user_info = self.db.get('SELECT * FROM User WHERE id=%s', user_id)
                if user_info is None:
                    #Cookie exists but user doesn't (Database deletion :()
                    return None
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
		
        def get_api_user(self):
            import hmac
            import hashlib
            import time
            from tornado.web import HTTPError
            try:
                digest = self.get_argument("api")
                user = self.get_argument("user")
                created_time = self.get_argument("time")
            except HTTPError:
                return None

            if time.time() - float(created_time) > 60:
                #Request is older than 1 minute
                return None

            #Get the URI without the api key parameter
            uri = self.request.uri.replace("api=%s"%digest, "")
            uri = uri.replace("&&", "&")
            uri = uri.replace("?&", "?")
            if uri[-1] == '&':
                uri = uri[0:-1]

            keys = self.db.query("SELECT api_key FROM ApiKey where user_id=%s;", user)
            for key in keys:
                hmac_obj = hmac.new(str(key['api_key']), uri, hashlib.sha256)
                ourdigest = hmac_obj.hexdigest()

                if ourdigest == digest:
                    #Authorized request
                    return user

            return None
