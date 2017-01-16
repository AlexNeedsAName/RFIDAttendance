import csv, datetime, sys

day = datetime.date.today().strftime("%m-%d-%y")

def checkForID(id):
	with open("database.csv", 'rb') as file:
		contents=file.read()
		if(id not in contents):
			return 1		#ID not found
		else:
			for line in contents.splitlines():
				if(id in line):
					try:
						name = line.split("\"")[3]
						return name
						break
					except IndexError:
						name = "User"
						return name
						break

def registerID(id):
	sys.stdout.write("Name: ")
	sys.stdout.flush()
	name = sys.stdin.readline().rstrip()

	with open("database.csv", 'a') as outFile:
		outFile.write("\n\""+ id + "\",\"" + name + "\"")

def markOffline(id):
	with open(day+".csv", 'a') as outFile:
		outFile.write("\"" + id + "\"\n")
