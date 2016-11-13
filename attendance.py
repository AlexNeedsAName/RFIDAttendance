#!/usr/bin/env python
import sys
import serial
import csv
import time
import datetime
import requests

s = serial.Serial('/dev/cu.usbmodem1411', 9600, timeout=1)
day = datetime.date.today().strftime("%m-%d-%y")
print(s.name)

attendanceForm = "1TyUw_tnk94NYrvrTONOZ2WxfCVtwljMd27GlTs-7r9w"
attendanceID = "entry.945552943"

ready = False
print("Waiting...")
while(not ready):
	read = s.readline()
	if("Ready" in read):
		ready = True

sys.stdout.write("Ready to take attendance.\n\n")
sys.stdout.flush()
try:
	while(True):
		read = s.readline()
		if("ID: " in read):
			id = read[4:].rstrip()
			with open("database.csv", 'rb') as file:
				contents = file.read()
				if(id not in contents):
					sys.stdout.write(id + "\nName: ")
					sys.stdout.write("Error, ID not found. Try scanning again, or if you are not registered, run the setup script.\n\n")
				else:
					for line in contents.splitlines():
						if(id in line):
							try:
								data = line.split("\"")
								sys.stdout.write("Welcome, " + data[3] + "!\n\n")
								sys.stdout.flush()
								break;
							except IndexError:
								sys.stdout.write("Welcome, User!\n\n")
								break
			
			requestString = "https://docs.google.com/forms/d/" + attendanceForm + "/formResponse?ifq&" + attendanceID + "=" + id
			requests.get(requestString)
	
			with open(day+".csv", 'a') as outFile:
				outFile.write("\n\""+ id + "\"")
except KeyboardInterrupt:
	sys.stdout.write("\n\nGoodbye!\n")
	sys.exit()
