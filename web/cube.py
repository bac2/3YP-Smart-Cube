from base_handler import BaseHandler
from data_objects import User, Transition, ProfileTransition, Profile, Cube
import tornado.web
import json
import datetime

class TransitionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, Transition):
            return { 'time':obj.time, 'position':obj.position, 'side_name':obj.side_name}

class BaseTransitionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, Transition):
            return { 'time':obj.time, 'position':obj.position }
        elif isinstance(obj, ProfileTransition):
            return { 'profile_id':obj.profile_id, 'time':obj.time, 'cube_id':obj.cube_id}

class CubeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Cube):
            return {'cube_id':obj.cube_id, 'code':obj.code, 'position':obj.rotation, 'last_transition':obj.last_transition, 'public':obj.public}

class UpdateHandler(BaseHandler):
    
        #Lists transitions for a given cube
        @tornado.web.authenticated
        def get(self, cube_code):
            transitions = self.fetch_transitions(cube_code)
            self.write(json.dumps(transitions, cls=BaseTransitionEncoder))

        def fetch_transitions(self, cube_code):
            transitions_info = self.db.query("SELECT * FROM Transition WHERE cube_id=(SELECT id FROM Cube WHERE unique_id=%s)", cube_code)

            transitions = []
            for transition_info in transitions_info:
                transition = Transition(transition_info)
                transitions.append(transition)
            
            return transitions
            
            

	#Receives an update from a cube
	def post(self, cube_code):
		import hmac
		import hashlib
		rotation = self.get_argument("rotation")
		time = self.get_argument("time")
		digest = self.get_argument("digest")
		#Get the cube key from the database
		cube_info = self.db.get("SELECT id, secret_key, owner FROM Cube WHERE unique_id=%s", cube_code)
		if not cube_info:
			#We don't know about this cube
			self.write("Unknown cube code")
			return
		hmac_obj = hmac.new(str(cube_info['secret_key']), str(rotation)+str(time), hashlib.sha224)
		our_digest = hmac_obj.hexdigest()
	
		if our_digest != digest:
			print "Digests don't match:", our_digest, digest
			return #Ignore it, it isn't from a cube we know!

		#Do some stuff here - Add a rotation to the database
		self.db.execute("INSERT INTO Transition (position, time, cube_id) VALUES (%s, %s, %s);", rotation, time, cube_info['id'])

        def check_events(self, cube_id, position):
           #Check for any events which are triggered 
           self.db.execute("UPDATE Event SET seen=NULL WHERE cube_id=(SELECT id FROM Cube WHERE unique_id=%s) AND rotation=%s", cube_code, position)
		

class RegisterHandler(BaseHandler):
	
	#Registers a cube to a user after scanning the QR code
	@tornado.web.authenticated
	def get(self, cube_code):
		cube = self.db.get("SELECT * FROM Cube WHERE unique_id=%s", cube_code)
		self.params['complete'] = False
		if cube:
			self.params['registered'] = True
		else:
			self.params['registered'] = False
			self.params['unique_code'] = cube_code
		self.render('register.html', **self.params)

class CubeHandler(BaseHandler):

        @tornado.web.authenticated
        def get(self):
            current_user = self.get_current_user()
            cubes = self.get_cubes()

            self.write(json.dumps(cubes, cls=CubeEncoder))

        @tornado.web.authenticated
	def post(self):
		import hashlib
		current_user = self.get_current_user()
		secret_code = hashlib.sha224(self.get_argument('unique_code')).hexdigest()
		self.db.execute("INSERT INTO Cube (secret_key, Owner, unique_id, public) VALUES (%s, %s, %s, 0);", secret_code, current_user.user_id, self.get_argument('unique_code')) 
		self.params['complete'] = True
		self.render('register.html', **self.params)



class ProfileTransitionHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, cube_code):
        profile_transitions_info = self.db.query("SELECT * FROM ProfileTransition WHERE cube_id=(SELECT id FROM Cube WHERE unique_id=%s);", cube_code)

        profile_transitions = []
        for profile_transition_info in profile_transitions_info:
            current = ProfileTransition(profile_transition_info)
            profile_transitions.append(current)

        self.write(json.dumps(profile_transitions, cls=BaseTransitionEncoder))

class TransitionsHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, cube_code, profile_transition_id):
        self.write(self.get_transitions(cube_code, profile_transition_id))

    def get_transitions(self, cube_code, profile_transition_id):
        transitions = self.db.query("SELECT position, time, cube_id, (SELECT (case position when 1 then side1 WHEN 2 THEN side2 WHEN 3 THEN side3 WHEN 4 THEN side4 WHEN 5 THEN side5 WHEN 6 THEN side6 end) AS side_name FROM ProfileTransition INNER JOIN Profile ON Profile.id = ProfileTransition.profile_id WHERE ProfileTransition.id=%s ORDER BY ProfileTransition.time DESC LIMIT 1) AS sidename FROM Transition WHERE cube_id=(SELECT id FROM Cube WHERE unique_id=%s) AND time BETWEEN (SELECT time FROM ProfileTransition WHERE id=%s AND ProfileTransition.cube_id=Transition.cube_id) AND (SELECT time FROM ProfileTransition WHERE id=%s AND ProfileTransition.cube_id=Transition.cube_id UNION (SELECT NOW() FROM DUAL) ORDER BY time ASC LIMIT 1);", str(profile_transition_id), str(cube_code), str(profile_transition_id), str(int(profile_transition_id)+1))

        transition_list = []
        for transition_info in transitions:
            transition_list.append( Transition(transition_info) )	
        return json.dumps(transition_list, cls=TransitionEncoder)


#Deals with changing and getting the profile of a cube
class ProfileHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self, cube_code):
                profile_id = self.get_argument("profile_id")
		
		profile_name = self.save_profile(cube_code, profile_id)
		
		self.write(profile_name)

	def save_profile(self, cube_code, profile_id):

		self.db.execute("INSERT INTO ProfileTransition (cube_id, profile_id, time) VALUES ((SELECT id FROM Cube WHERE unique_id=%s), %s, NOW());", cube_code, profile_id)

		profile = self.db.get("SELECT * FROM Profile WHERE id = %s", profile_id)
		return profile['name']

class PublicHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self, cube_code):
                value = self.get_argument("value")
		self.save_public(cube_id, value)
		if value == '1':
			response='Yes'
		else:
			response='No'
		
		self.write(response)

	def save_public(self, cube_id, value):
		self.db.execute("UPDATE Cube SET public=%s WHERE unique_id=%s", value, cube_code)

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

        @tornado.web.authenticated
        def post(self, cube_code):
                side = self.get_argument("side")
                action = self.get_argument("action")
                profile_id = self.get_argument("profile_id")
                current_user = self.get_current_user()

                #First, check the users are friends
                friend = self.db.query("SELECT * FROM Friend WHERE (user1=%s AND user2=(SELECT owner FROM Cube WHERE unique_id=%s)) OR (user1 IN (SELECT owner FROM Cube WHERE unique_id=%s) AND user2=%s);", current_user.user_id, cube_code, current_user.user_id, cube_code);
                if friend is None:
                    #Not friends!
                    return
                
                self.db.execute("INSERT INTO Event (cube_id, owner, action, rotation, profile_id) VALUES (%s, %s, %s, %s, %s);", cube_id, current_user.user_id, action, side, profile_id);
