import time
import pickle
from cube import Rotation

class Log:
	def __init__(self, logfile='RotationData.log'):
		#Open a logfile for reading and writing
		self.logfile = open(logfile, 'w+')
		#We load the file list...
		try:
			self.logdata = pickle.load(self.logfile)
			self.logfile.seek(0)
		except EOFError: #Empty file, start again
			self.logdata = []
	
	def write_to_log(self, rotation):
		try:
			self.logdata.append(rotation)
			print "Log data is: ", self.logdata
			self.logfile.seek(0)
			pickle.dump(self.logdata, self.logfile)
		except IOError, e:
			print "IOError:", e

	def clear_log(self):
		self.logdata = []
		self.logfile.seek(0)
		pickle.dump(self.logdata, self.logfile)
		print 'Cleared log... Log is: ', self.logdata
	
	def get_backlog(self):
		try:
			#We get a list...
			data = pickle.load(self.logfile)
			self.logfile.seek(0)
			self.clear_log()
			return data
		except EOFError:
			#No more backlog!
			return False

	def __del__(self):
		self.logfile.close()

	
		
if(__name__ == '__main__'):
	log = Log()
	rot = Rotation(time.time(), 3)
	#log.write_to_log(rot)
	print log.get_backlog()
		
