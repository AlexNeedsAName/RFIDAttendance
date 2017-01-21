#!/usr/bin/env python 
import sys
import forms, database

configFile = "config.yml"

sys.argv.pop(0)

attendance = forms.form(configFile, "attendance")

for fileName in sys.argv:
	date = fileName[:-4]
	print("Uploading IDs from " + date)
	error = attendance.submit("Start of " + date)
	if(error):
		print("Could not submit form. Fix your internet.")
		sys.exit(1)
	with open(fileName, 'rb') as file:
		ids = file.read().splitlines()
		for id in ids:
			id = id.translate(None, '"')
			print("	Uploading " + id)
			error = attendance.submit(id)
			if(error):
				print("Could not submit form. Fix your internet.")
				sys.exit(1)
	error = attendance.submit("End of " + date)
	if(error):
		print("Could not submit form. Fix your internet.")
		sys.exit(1)
	print("")
