# I2C writes =D0=0                                                                                                                                   
# MMA7455 I2C address 1D (3A ,3B) write , read                                                                                                       
# AN3745 app note for calibration                                                                                                                    
# byte read , write 1D , write address, read 1D ,DATA                                                                                                
# Byte write, write 1D , write address, write data.                                                                                                  
# addresses,                                                                                                                                         
# 06 XOUT8                                                                                                                                           
# 07 YOUT8                                                                                                                                           
# 08 ZOUT8                                                                                                                                           
# 09 STATUS  D0 1=data ready                                                                                                                         
# 0A detection source                                                                                                                                
# 0F who am i                                                                                                                                        
# 16 Mode Control  x1000101 measure 2gmode 0x45                                                                                                      
# 16 Mode Control  x1000001 measure 8gmode 0x41                                                                                                      
# 16 Mode Control  x1000100 standby 2gmode 0x84                                                                                                      
# 16 Mode Control  x1010101 ston measure 2gmode 0x55                                                                                                 
# 18 Control1  D7 filter 0=62Hz,1=125Hz other 0                                                                                                      
# 19 Control2  default 0                                                                                                                             
#!/usr/bin/python                                                                                                                                    
import smbus
import time
import os

class Accel:

	def __init__(self):
	   	self.bus = smbus.SMBus(1)

	def setUp(self):

        # Setup the Mode
		self.bus.write_byte_data(0x1D,0x16,0x55)

        # Setup Calibration
		self.bus.write_byte_data(0x1D,0x10,0)
		self.bus.write_byte_data(0x1D,0x11,0)
		self.bus.write_byte_data(0x1D,0x12,0)
		self.bus.write_byte_data(0x1D,0x13,0)
		self.bus.write_byte_data(0x1D,0x14,0)
		self.bus.write_byte_data(0x1D,0x15,0)
 
	def getValueX(self):
		return self.bus.read_byte_data(0x1D,0x06)
 
	def getValueY(self):
		return self.bus.read_byte_data(0x1D,0x07)
 
	def getValueZ(self):
		return self.bus.read_byte_data(0x1D,0x08)
		
	def calibX(self):
		raw_input("Place device upwards on a flat surface.")
		self.XPos = [80*self.getValueX()/256, 80*self.getValueY()/256, 80*self.getValueZ()/256]
		raw_input("Place device upside down on a flat surface.")
		self.XNeg = [80*self.getValueX()/256, 80*self.getValueY()/256, 80*self.getValueZ()/256]

	def calibY(self):
		raw_input("Place device on it's side on a flat surface")
		self.YPos = [80*self.getValueX()/256, 80*self.getValueY()/256, 80*self.getValueZ()/256]
		raw_input("Place device on the opposite side on a flat surface")
		self.YNeg = [80*self.getValueX()/256, 80*self.getValueY()/256, 80*self.getValueZ()/256]
	
	def calibZ(self):
		raw_input("Place device endways on a flat surface")
		self.ZPos =[80*self.getValueX()/256, 80*self.getValueY()/256, 80*self.getValueZ()/256]
		raw_input("Place device on the opposite side on a flat surface")
		self.ZNeg =[80*self.getValueX()/256, 80*self.getValueY()/256, 80*self.getValueZ()/256]

	def determineDirection(self):
		currentX = 80*self.getValueX()/256
		currentY = 80*self.getValueY()/256
		currentZ = 80*self.getValueZ()/256
		#We want to check if it matchs the calibration...
		#First, X... (Rotates around Z Axis)
		if( self.XPos[0]-10 < currentX <= self.XPos[0]+10
			and self.XPos[1]-10 < currentY <= self.XPos[1]+10 ):
			#Either XPos or XNeg
			if( self.XPos[2]-10 < currentZ <= self.XPos[2]+10 ):
				return "X Up"
			if( self.XNeg[2]-10 < currentZ <= self.XNeg[2]+10 ):
				return "X Down"

		#Then Y... (Rotates around Y axis)
		elif( self.YPos[0]-10 < currentX <= self.YPos[0]+10
			and self.YPos[2]-10 < currentZ <= self.YPos[2]+10 ):
			#Either YPos or YNeg
			if( self.YPos[1]-10 < currentY <= self.YPos[1]+10 ):
				return "Y Up"
			if( self.YNeg[1]-10 < currentY <= self.YNeg[1]+10 ):
				return "Y Down"

		#Then Z... (Rotates around X axis)
		elif( self.ZPos[1]-10 < currentY <= self.ZPos[1]+10
			and self.ZPos[2]-10 < currentZ <= self.ZPos[2]+10 ):
			#Either ZPos or ZNeg
			if( self.ZPos[0]-10 < currentX <= self.ZPos[0]+10 ):
				return "Z Up"
			if( self.ZNeg[0]-10 < currentX <= self.ZNeg[0]+10 ):
				return "Z Down"

		else:
			return "Unknown"


MMA7455 = Accel()
MMA7455.setUp()
MMA7455.calibX()
MMA7455.calibY()
MMA7455.calibZ()
 
for a in range(100):
	x = MMA7455.getValueX()
	y = MMA7455.getValueY()
	z = MMA7455.getValueZ()
 
	print "x=", x , "\t[" , "=" * (80 * x / 256) , " " *  (80 - (80 * x / 256)) , "] " , (80 * x / 256) , "%"
	print "y=", y , "\t[" , "=" * (80 * y / 256) , " " *  (80 - (80 * y / 256)) , "] " , (80 * y / 256) , "%"
	print "z=", z , "\t[" , "=" * (80 * z / 256) , " " *  (80 - (80 * z / 256)) , "] " , (80 * z / 256) , "%"
	print MMA7455.determineDirection()
	time.sleep(2.0)
#	os.system('clear')
