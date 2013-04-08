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
                config.read('/home/pi/3YP/cube/cube.conf')

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
		lowerBound = 0.9
		upperBound = 1.1
		currentX = self.accel.getPercentX()
		currentY = self.accel.getPercentY()
		currentZ = self.accel.getPercentZ()
		#We want to check if it matchs the calibration...

		#First, X UP... (Rotates around Z Axis)
		XDiff = abs(self.XPos[0] - currentX)
		YDiff = abs(self.XPos[1] - currentY)
		ZDiff = abs(self.XPos[2] - currentZ)
		if( (XDiff < 10 or XDiff > 90)
			and (YDiff < 10 or YDiff > 90)
			and (ZDiff < 10 or ZDiff > 90) ):
				self.currentRotation = Cube.XUP	

		#Then X DOWN...
		XDiff = abs(self.XNeg[0] - currentX)
		YDiff = abs(self.XNeg[1] - currentY)
		ZDiff = abs(self.XNeg[2] - currentZ)
		
		if( (XDiff < 10 or XDiff > 90)
			and (YDiff < 10 or YDiff > 90)
			and (ZDiff < 10 or ZDiff > 90) ):
				self.currentRotation = Cube.XDOWN

		#Then Y Pos... (Rotates around Y axis)
		XDiff = abs(self.YPos[0] - currentX)
		YDiff = abs(self.YPos[1] - currentY)
		ZDiff = abs(self.YPos[2] - currentZ)
		
		if( (XDiff < 10 or XDiff > 90)
			and (YDiff < 10 or YDiff > 90)
			and (ZDiff < 10 or ZDiff > 90) ):
				self.currentRotation = Cube.YUP

		#Then YNeg...
		XDiff = abs(self.YNeg[0] - currentX)
		YDiff = abs(self.YNeg[1] - currentY)
		ZDiff = abs(self.YNeg[2] - currentZ)
		
		if( (XDiff < 10 or XDiff > 90)
			and (YDiff < 10 or YDiff > 90)
			and (ZDiff < 10 or ZDiff > 90) ):
				self.currentRotation = Cube.YDOWN

		#Then ZPos... (Rotates around X axis)
		XDiff = abs(self.ZPos[0] - currentX)
		YDiff = abs(self.ZPos[1] - currentY)
		ZDiff = abs(self.ZPos[2] - currentZ)
		
		if( (XDiff < 10 or XDiff > 90)
			and (YDiff < 10 or YDiff > 90)
			and (ZDiff < 10 or ZDiff > 90) ):
				self.currentRotation = Cube.ZUP

		#Then ZNeg
		XDiff = abs(self.ZNeg[0] - currentX)
		YDiff = abs(self.ZNeg[1] - currentY)
		ZDiff = abs(self.ZNeg[2] - currentZ)
		
		if( (XDiff < 10 or XDiff > 90)
			and (YDiff < 10 or YDiff > 90)
			and (ZDiff < 10 or ZDiff > 90) ):
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
	cube = Cube()
	cube.calibX()
	cube.calibY()
	cube.calibZ()
	print cube.XPos, cube.XNeg, cube.YPos, cube.YNeg, cube.ZPos, cube.ZNeg

	import time
	import os

	MMA7455 = cube.accel 
	 
	for a in range(10000):
		x = MMA7455.getPercentX()
		y = MMA7455.getPercentY()
		z = MMA7455.getPercentZ()
	 
		print "x=", x , "\t[" , "=" * (x) , " " *  (100 - x) , "] " , x , "%"
		print "y=", y , "\t[" , "=" * (y) , " " *  (100 - y) , "] " , y , "%"
		print "z=", z , "\t[" , "=" * (z) , " " *  (100 - z) , "] " , z , "%"
		cube.check_rotation()
		print cube
		print cube.XPos, cube.XNeg, cube.YPos, cube.YNeg, cube.ZPos, cube.ZNeg
		time.sleep(0.1)
		os.system('clear')

