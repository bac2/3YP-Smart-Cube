#!/usr/bin/python                                                                                                                                    
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

import smbus
import time
import os

class Accel:

	def __init__(self):
	   	self.bus = smbus.SMBus(1)
		self.setUp()

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
	
	def getPercentX(self):
		return 100*self.getValueX()/256
 
	def getValueY(self):
		return self.bus.read_byte_data(0x1D,0x07)

	def getPercentY(self):
		return 100*self.getValueY()/256
 
	def getValueZ(self):
		return self.bus.read_byte_data(0x1D,0x08)

	def getPercentZ(self):
		return 100*self.getValueZ()/256
		

if( __name__ == '__main__'):
	MMA7455 = Accel()

	 
	for a in range(10000):
		x = MMA7455.getValueX()
		y = MMA7455.getValueY()
		z = MMA7455.getValueZ()
	 
		print "x=", x , "\t[" , "=" * (80 * x / 256) , " " *  (80 - (80 * x / 256)) , "] " , (80 * x / 256) , "%"
		print "y=", y , "\t[" , "=" * (80 * y / 256) , " " *  (80 - (80 * y / 256)) , "] " , (80 * y / 256) , "%"
		print "z=", z , "\t[" , "=" * (80 * z / 256) , " " *  (80 - (80 * z / 256)) , "] " , (80 * z / 256) , "%"
		time.sleep(0.1)
		os.system('clear')
