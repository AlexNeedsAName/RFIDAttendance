#!/usr/bin/env python
import sys
import serial
import csv
import time
import requests
import glob
import yaml
from datetime import timedelta, datetime

with open("config.yml", 'r') as config:
	try:
		configData = yaml.safe_load(config)
	except yaml.YAMLError as e:
		sys.stdout.write("Failed to parse config file.\n")
		print e
		sys.exit(1)

setupForm = configData["registration"]["form"]
setupName = configData["registration"]["name"]
setupID   = configData["registration"]["id"]

attendanceForm = configData["attendance"]["form"]
attendanceID   = configData["attendance"]["id"]

online = True

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

ready = False
print("Waiting...")
while(not ready):
	read = s.readline()
	if("Ready" in read):
		ready = True

print("Ready to register ID tags.")
sys.stdout.write("\nID: ")
sys.stdout.flush()
lastScanTime = datetime.now()
minScanTime = timedelta(seconds=1) 

try:
	while(True):
		read = s.readline()
		if("ID: " in read):
			currentScanTime = datetime.now()
			if(currentScanTime - lastScanTime > minScanTime):
				id = read[4:].rstrip()
				with open("database.csv", 'rb') as file:
					contents = file.read()
					if(id not in contents):
						sys.stdout.write(id + "\nName: ")
						sys.stdout.flush()
						name = sys.stdin.readline().rstrip()
						
						sys.stdout.write("\n")
						
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
			lastScanTime = datetime.now()
except KeyboardInterrupt:
	sys.stdout.write("\n\nDone!\n")
	sys.stdout.flush
	sys.exit()
