import csv, datetime, sys

day = datetime.date.today().strftime("%m-%d-%y")

def getPeople():
	people = []
	with open('database.csv', 'rb') as f:
    		reader = csv.reader(f)
    		database = list(reader)
		for person in database:
			try:
				people.append([person[1],person[0]])
			except IndexError:
				pass
	people.sort()
	return people

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

def checkForMatches(input):
	people = getPeople()
	matches = []
	i=1
	for person in people:
		try:
			if(i<=9 and input.lower() == person[0][:len(input)].lower()): #if person's name starts with input and we have less than 9 matches
				matches.append(person)
				print "["+str(i)+"] " + person[0] + "\t("+str(person[1])+")"
				i+=1
	
		except IndexError:
			pass
	return matches	

def registerID(id):
	sys.stdout.write("Name: ")
	sys.stdout.flush()
	name = sys.stdin.readline().rstrip()

	with open("database.csv", 'a') as outFile:
		outFile.write("\n\""+ id + "\",\"" + name + "\"")
	return name

def markOffline(id):
	with open(day+".csv", 'a') as outFile:
		outFile.write("\"" + id + "\"\n")
