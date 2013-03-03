from base_handler import BaseHandler
import tornado.web
class UpdateHandler(BaseHandler):
	
	#Receives an update from a cube
	def post(self, unique_code):
		import hmac
		import hashlib
		rotation = self.get_argument("rotation")
		time = self.get_argument("time")
		digest = self.get_argument("digest")
		#Get the cube key from the database
		cube_info = self.db.get("SELECT id, secret_key, owner FROM Cube WHERE unique_id=%s", unique_code)
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
           self.db.execute("UPDATE Event SET seen=NULL WHERE cube_id=%s AND rotation=%s", cube_id, position)
		

class RegisterHandler(BaseHandler):
	
	#Registers a cube to a user after scanning the QR code
	@tornado.web.authenticated
	def get(self, unique_code):
		cube = self.db.get("SELECT * FROM Cube WHERE unique_id=%s", unique_code)
		self.params['complete'] = False
		if cube:
			self.params['registered'] = True
		else:
			self.params['registered'] = False
			self.params['unique_code'] = unique_code
		self.render('register.html', **self.params)

	def post(self):
		import hashlib
		current_user = self.get_current_user()
		secret_code = hashlib.sha224(self.get_argument('unique_code')).hexdigest()
		self.db.execute("INSERT INTO Cube (secret_key, Owner, unique_id) VALUES (%s, %s, %s);", secret_code, current_user.user_id, self.get_argument('unique_code')) 
		self.params['complete'] = True
		self.render('register.html', **self.params)

