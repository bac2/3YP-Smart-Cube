from mma7455 import Accel 
import ConfigParser
import json

class Rotation:
	def __init__(self, rotation, time):
		self.time = time
		self.rotation = rotation
	
class Cube:
	UNKNOWN = 0;
	XUP = 1;
	XDOWN = 2;
	YUP = 3;
	YDOWN = 4;
	ZUP = 5;
	ZDOWN = 6;

	def __init__(self):
                config = ConfigParser.RawConfigParser()
                config.read('cube.conf')

		self.code = config.get("cube", "code")
		self.secret_code = config.get("cube", "secret")
		self.accel = Accel()
		self.currentRotation = 0;
		#Some preconfigured values...
		self.XPos = json.loads(config.get("cube", "XPos"))
		self.XNeg = json.loads(config.get("cube", "XNeg"))
		self.YPos = json.loads(config.get("cube", "YPos"))
		self.YNeg = json.loads(config.get("cube", "YNeg"))
		self.ZPos = json.loads(config.get("cube", "ZPos"))
		self.ZNeg = json.loads(config.get("cube", "ZNeg"))

	def get_rotation(self):
		return self.currentRotation
	
	def calibX(self):
		#Raw input accepts empty input
		raw_input("Place device upwards on a flat surface.")
		self.XPos = [self.accel.getPercentX(), self.accel.getPercentY(), self.accel.getPercentZ()]
		raw_input("Place device upside down on a flat surface.")
		self.XNeg = [self.accel.getPercentX(), self.accel.getPercentY(), self.accel.getPercentZ()]

	def calibY(self):
		raw_input("Place device on it's side on a flat surface")
		self.YPos = [self.accel.getPercentX(), self.accel.getPercentY(), self.accel.getPercentZ()]
		raw_input("Place device on the opposite side on a flat surface")
		self.YNeg = [self.accel.getPercentX(), self.accel.getPercentY(), self.accel.getPercentZ()]
	
	def calibZ(self):
		raw_input("Place device endways on a flat surface")
		self.ZPos = [self.accel.getPercentX(), self.accel.getPercentY(), self.accel.getPercentZ()]
		raw_input("Place device on the opposite side on a flat surface")
		self.ZNeg = [self.accel.getPercentX(), self.accel.getPercentY(), self.accel.getPercentZ()]



	def check_rotation(self):
		currentX = self.accel.getPercentX()
		currentY = self.accel.getPercentY()
		currentZ = self.accel.getPercentZ()
		#We want to check if it matchs the calibration...
		#First, X... (Rotates around Z Axis)
		if( self.XPos[0]-10 < currentX <= self.XPos[0]+10
			and self.XPos[1]-10 < currentY <= self.XPos[1]+10 ):
			#Either XPos or XNeg
			if( self.XPos[2]-10 < currentZ <= self.XPos[2]+10 ):
				self.currentRotation = Cube.XUP	
			if( self.XNeg[2]-10 < currentZ <= self.XNeg[2]+10 ):
				self.currentRotation = Cube.XDOWN

		#Then Y... (Rotates around Y axis)
		elif( self.YPos[0]-10 < currentX <= self.YPos[0]+10
			and self.YPos[2]-10 < currentZ <= self.YPos[2]+10 ):
			#Either YPos or YNeg
			if( self.YPos[1]-10 < currentY <= self.YPos[1]+10 ):
				self.currentRotation = Cube.YUP
			if( self.YNeg[1]-10 < currentY <= self.YNeg[1]+10 ):
				self.currentRotation = Cube.YDOWN

		#Then Z... (Rotates around X axis)
		elif( self.ZPos[1]-10 < currentY <= self.ZPos[1]+10
			and self.ZPos[2]-10 < currentZ <= self.ZPos[2]+10 ):
			#Either ZPos or ZNeg
			if( self.ZPos[0]-10 < currentX <= self.ZPos[0]+10 ):
				self.currentRotation = Cube.ZUP
			if( self.ZNeg[0]-10 < currentX <= self.ZNeg[0]+10 ):
				self.currentRotation = Cube.ZDOWN

		else:
			currentRotation = Cube.UNKNOWN

	def __str__(self):
		if( self.currentRotation == Cube.XUP):
			return "X UP"
		if( self.currentRotation == Cube.XDOWN ):
			return "X DOWN"
		if( self.currentRotation == Cube.YUP ):
			return "Y UP"
		if( self.currentRotation == Cube.YDOWN ):
			return "Y DOWN"
		if( self.currentRotation == Cube.ZUP ):
			return "Z UP"
		if( self.currentRotation == Cube.ZDOWN ):
			return "Z DOWN"
		return "UNKNOWN"

if __name__=='__main__':
	cube = Cube("123")
	cube.calibX()
	cube.calibY()
	cube.calibZ()
	print cube.XPos, cube.XNeg, cube.YPos, cube.YNeg, cube.ZPos, cube.ZNeg
