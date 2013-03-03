import time
import pickle
import logging
from cube import Rotation

class Log:
	def __init__(self, logfile='/home/pi/3YP/cube/RotationData.log'):
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
			logging.info("Log data is: ", self.logdata)
			self.logfile.seek(0)
			pickle.dump(self.logdata, self.logfile)
			logging.info("Written to log")
			print "Written"
		except IOError, e:
			logging.error("IOError:"+ str(e))
			print "IOError", e
		except StandardError, e:
			print "StdError", e
			logging.error("StandardError Writing to log: "+ str(e))

	def clear_log(self):
		#Empties the log file on disk
		self.logdata = []
		self.logfile.seek(0)
		pickle.dump(self.logdata, self.logfile)
		print 'Cleared log... Log is now empty'
	
	def get_backlog(self):
		try:
			#We get a list...
			self.logfile.seek(0)
			data = pickle.load(self.logfile)
			self.clear_log()
			print "Backlog fetched", data
			return data
		except EOFError:
			#No more backlog!
			return False

	def __del__(self):
		self.logfile.close()

	
		
if(__name__ == '__main__'):
	log = Log("testLog.log")
	rot = Rotation(3, time.time())
	log.write_to_log(rot)
	print log.get_backlog()
		
