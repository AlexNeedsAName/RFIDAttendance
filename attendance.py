#!/usr/bin/env python
import sys, serial, csv, time, requests, glob, yaml, argparse, datetime

#Parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument("-o", "--offline", help="run in offline mode", action="store_true")
parser.add_argument("-r", "--register", help="register new users", action="store_true")
args = parser.parse_args()
online = not(args.offline)

#read from config
with open("config.yml", 'r') as config:
	try:
		configData = yaml.safe_load(config)
	except yaml.YAMLError as e:
		sys.stdout.write("Failed to parse config file.\n")
		sys.exit(1)

setupForm = configData["registration"]["form"]
setupName = configData["registration"]["name"]
setupID   = configData["registration"]["id"]

attendanceForm = configData["attendance"]["form"]
attendanceID   = configData["attendance"]["id"]

#Connect to Arduino
if sys.platform.startswith('win'):
	ports = ['COM%s' % (i + 1) for i in range(256)]
else:
	ports = glob.glob("/dev/tty.usbmodem*")
connected = False
for port in ports:
	if(not connected):
		try:
			s = serial.Serial(port, 9600, timeout=1)
			connected = True
		except:
			connected = False
if(not connected):
	print("Failed to autodetect serial port.")
	sys.exit()
print("Connected on " + s.name)

#Wait for Arduino
ready = False
print("Waiting...")
while(not ready):
	read = s.readline()
	if("Ready" in read):
		ready = True

if(args.register):
	sys.stdout.write("Ready to register ID tags.")
else:
	sys.stdout.write("Ready to take attendance.")
sys.stdout.write("\nID: ")
sys.stdout.flush()

day = datetime.date.today().strftime("%m-%d-%y")
lastScanTime = datetime.datetime.now()
minScanTime = datetime.timedelta(seconds=1) 

#Main Loop
try:
	while(True):
		read = s.readline()
		if("ID: " in read):
			currentScanTime = datetime.datetime.now()
			if(currentScanTime - lastScanTime > minScanTime):
				id = read[4:].rstrip()
				sys.stdout.write(id + "\n")
				with open("database.csv", 'rb') as file:
					if(args.register):
						contents = file.read()
						if(id not in contents):
							sys.stdout.write("Name: ")
							sys.stdout.flush()
							name = sys.stdin.readline().rstrip()
						
							if(online):
								try:
									request1String = "https://docs.google.com/forms/d/" + setupForm + "/formResponse?ifq&" + setupID + "=" + id + "&" + setupName + "=" + name
									request2String = "https://docs.google.com/forms/d/" + attendanceForm + "/formResponse?ifq&" + attendanceID + "=" + id
				
									requests.get(request1String)
									requests.get(request2String)
								except requests.exceptions.ConnectionError:
									online = False
									sys.stdout.write("\nCould not connect to the internet, running in offline mode.\n")
	
							with open("database.csv", 'a') as outFile:
								outFile.write("\n\""+ id + "\",\"" + name + "\"")
			
							sys.stdout.write("\nID: ")
							sys.stdout.flush()
						else:
							for line in contents.splitlines():
								if(id in line):
									data = line.split("\"")
									sys.stdout.write(data[1] + " is already registered to " + data[3] + "\n\nID: ")
									sys.stdout.flush()
					else:
						contents=file.read()
						if(id not in contents):
							sys.stdout.write("Error, ID not found. Try scanning again, or if you are not registered, run the setup script.\n\nID: ")
							sys.stdout.flush()
						else:
							for line in contents.splitlines():
								if(id in line):
									try:
										data = line.split("\"")
										sys.stdout.write("Welcome, " + data[3] + "!\n\n")
										sys.stdout.flush()
										break
									except IndexError:
										sys.stdout.write("Welcome, User!\n\n")
										sys.stdout.flush()
										break
							if(online):
								try:
									requests.get("https://docs.google.com/forms/d/" + attendanceForm + "/formResponse?ifq&" + attendanceID + "=" + id)
								except requests.exceptions.ConnectionError:
									online = False
									sys.stdout.write("\nCould not connect to the internet, running in offline mode.\n")
									with open(day+".csv", 'a') as outFile:
										outFile.write("\n\""+ id + "\"")
							else:
								with open(day+".csv", 'a') as outFile:
									outFile.write("\n\""+ id + "\"")
							sys.stdout.write("ID: ")
							sys.stdout.flush()
			lastScanTime = datetime.datetime.now()
except KeyboardInterrupt:
	sys.stdout.write("\n\nDone!\n")
	sys.stdout.flush
	sys.exit()
