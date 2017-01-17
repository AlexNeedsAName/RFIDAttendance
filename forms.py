import requests, yaml

offline = False

class form():
	def __init__(self, configFile, type):
		with open(configFile, 'r') as config:
		        try:
       				configData = yaml.safe_load(config)
				self.config = configData[type]
        		except yaml.YAMLError as e:
                		print("Failed to parse config file.\n")
                		sys.exit(1)

	def submit(self, id, name=None):
		global offline
		if(not offline):
			request = "https://docs.google.com/forms/d/" + self.config["form"] + "/formResponse?ifq&" + self.config["id"] + "=" +id
			if(name is not None):
				request += "&" + self.config["name"] + name
			try:
				status = str(requests.get(request))[11:14]
				if("2" != status[:1]):
					print("Error " + status + ", running in offline mode.")
					offline = True
					return 1
				return 0
			except requests.exceptions.ConnectionError:
				offline = True
				print("Could not connect to the internet, running in offline mode.")
				return 1

		else:
			 return 1

def setOffline():
	print("Running in offline mode.")
	global offline
	offline = True
