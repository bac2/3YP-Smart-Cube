import time
import json

class Log:
	def __init__(self, logfile='RotationData.log'):
		self.logfile = open(logfile, 'r+')
		data = self.logfile.read();
	
	def write_to_log(self, data):
		try:
			self.logfile.write( json.dumps(data) )
		except IOError:
			print "ARGHHH!!!"
	
	
		
log = Log()
log.write_to_log({'right':3})
		
