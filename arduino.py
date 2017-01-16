import sys, serial, glob, datetime

class arduino:
	connected = False
	minScanTime = datetime.timedelta(seconds=1)
	lastScanTime = datetime.datetime.now() - minScanTime

	def autodetectSerial(self):
		if(self.connected):
			print("Already connected on " + self.serialCon.name)
			return 0
		if sys.platform.startswith('win'):
			ports = ['COM%s' % (i + 1) for i in range(256)]
		else:
		        ports = glob.glob("/dev/tty.usbmodem*")
	
		for port in ports:
		        if(not self.connected):
		               	try:
	             	           self.serialCon = serial.Serial(port, 9600, timeout=1)
		     	           self.connected = True
				except serial.serialutil.SerialException:
					print port + " is busy"
	
		if(self.connected):
			print("Connected on " + self.serialCon.name)
			return 0
		else:
		        print("Failed to autodetect serial port.")
		        return 1

	def waitForString(self, string):
		ready = False
		print("Waiting...")
		while(not ready):
		        read = self.serialCon.readline()
		        if(string in read):
	        	        ready = True

	def getID(self):
		id = None
		while (id == None):
			read = self.serialCon.readline()
			if("ID: " in read):
				self.currentScanTime = datetime.datetime.now()
				if(self.currentScanTime - self.lastScanTime > self.minScanTime):
					id = read[4:].rstrip()
					return id
				else:
					self.lastScanTime = datetime.datetime.now() #If another ID is scanned within the minScanTime, reset the timer
	def scanFinished(self):
		self.lastScanTime = datetime.datetime.now()
		sys.stdout.write("\nID: ")
