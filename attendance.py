#!/usr/bin/env python
import sys, csv, argparse, datetime
import arduino, database, forms

configFile = "config.yml"

#Parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument("-o", "--offline", help="run in offline mode", action="store_true")
args = parser.parse_args()
if(args.offline):
	forms.setOffline()

scanner = arduino.arduino()

if(scanner.autodetectSerial()):
	sys.exit()

scanner.waitForString("Ready")

print("Ready to take attendance.\n")
sys.stdout.write("ID: ")
sys.stdout.flush()

register = forms.form(configFile, "registration")
attendance = forms.form(configFile, "attendance")
#Main Loop
try:
	while(True):
		id = scanner.getID()
		print id
		
		name = database.checkForID(id)
		if(name == 1):
			print("You don't seem to be in the database. Type your name to register.")
			name = database.registerID(id)
			error = register.submit(id, name)
			if(error):
				print("We are currently offline, but you will be registered once we regain connection, " + name)
		else:
			print("Welcome, " + name)
		error = attendance.submit(id)
		if(error):
			database.markOffline(id)

		scanner.scanFinished()
		sys.stdout.flush()
except KeyboardInterrupt:
	sys.stdout.write("\n\nDone!\n")
	sys.stdout.flush()
	sys.exit()
