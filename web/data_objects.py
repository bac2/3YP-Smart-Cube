
class User():
	def __init__(self,user_info):
		self.name = user_info['name']
		self.email = user_info['email']
		self.user_id = user_info['id']
		#set elsewhere
		self.cubes = None
	
	def __str__(self):
		return str({'name':self.name, 'email':self.email, 'user_id':self.user_id})

class Profile():
	def __init__(self, profile_info):
		self.profile_id = profile_info['id']
		self.describe_line = profile_info['describe_line']
		self.creator_id = profile_info['creator_id']
		self.name = profile_info['name']
		self.sides = [profile_info['side1'], profile_info['side2'], profile_info['side3'],
				profile_info['side4'], profile_info['side5'], profile_info['side6']
			     ]

class Cube():
	def __init__(self, cube_info):
		self.cube_id = cube_info['id']
		self.code = cube_info['unique_id']
		self.rotation = cube_info['position']
		self.last_transition = cube_info['last_transition']
		self.public = cube_info['public']
		#These are set externally
		self.profile = None
		self.corresponding_profile = None

class Transition():
	def __init__(self, transition_info):
		self.time = transition_info['time']
		self.position = transition_info['position']
		self.cube_id = transition_info['cube_id']
		self.side_name = transition_info['sidename']
