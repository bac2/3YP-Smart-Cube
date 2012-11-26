from mma7455 import Accel 


class Cube:
	UNKNOWN = 0;
	XUP = 1;
	XDOWN = 2;
	YUP = 3;
	YDOWN = 4;
	ZUP = 5;
	ZDOWN = 6;

	def __init__(self):
		self.accel = Accel()
		self.currentRotation = 0;
		#Some preconfigured values...
		self.XPos = [67, 65, 33]
		self.XNeg = [67, 65, 77]
		self.YPos = [64, 44, 15]
		self.YNeg = [64, 3, 15]
		self.ZPos = [45, 65, 13]
		self.ZNeg = [5, 65, 13]

	def getRotation(self):
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



	def checkRotation(self):
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

	def str(self):
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
	

if(__name__ == '__main__'):
	import time
	cube = Cube()
	while True:
		cube.checkRotation()
		print cube.str()
		time.sleep(1.0)