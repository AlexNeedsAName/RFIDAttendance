#!/usr/bin/env python
import csv, yaml, sys, os, requests, getch
clear = "clear"
if(os.name == "nt"):
    clear = "cls"

with open("config.yml", 'r') as config:
    try:
        configData = yaml.safe_load(config)
    except Exception:
        sys.stdout.write("Failed to parse config file.\n")
        sys.exit(1)

attendanceForm = configData["attendance"]["form"]
attendanceID   = configData["attendance"]["id"]

def checkForMatches(substring, people):
    matches = []
    i=1
    for person in people:
        try:
            if(i<=9 and input.lower() == person[0][:len(input)].lower()): #if person's name starts with input
                matches.append(person)
                print "["+str(i)+"] " + person[0] + "\t("+str(person[1])+")"
                i+=1
        except IndexError:
            pass
    return matches

global online
online = True

def markPresent(id):
    global online
    if(online):
        try:
            requests.get("https://docs.google.com/forms/d/" + attendanceForm + "/formResponse?ifq&" + attendanceID + "=" + id)
        except requests.exceptions.ConnectionError:
            online = False
            sys.stdout.write("\nCould not connect to the internet, running in offline mode.\n")
            with open(day+".csv", 'a') as outFile:
                outFile.write("\n\""+ id + "\"")


with open('database.csv', 'rb') as f:
    reader = csv.reader(f)
    database = list(reader)
people = []
for person in database:
    try:
        people.append([person[1],person[0]])
    except IndexError:
        pass
del database
people.sort()

matches = []
input = ""

#this will be in a loop that is reading input characters
os.system(clear)
print("Manual Entry:\n")
while True:
    inputChar = str(getch.getch())
    os.system(clear)
    print("Manual Entry:\n")
    if(inputChar.isalpha()):
        input+=str(inputChar)
        print(input)
        matches = checkForMatches(input, people)
    elif(ord(inputChar) == 32): #Spacebar
        input+=" "
        print input
        matches = checkForMatches(input, people)
    elif(ord(inputChar) == 127): #Backspace
        input = input[:-1]
        print(input)
        if(input!=""):
            matches = checkForMatches(input, people)
        else:
            matches = []
    elif(ord(inputChar) == 3): #Keyboard Interrupt
        break
    elif(inputChar.isdigit()):
        try:
            input = ""
            markPresent(matches[int(inputChar)-1][1])
            print("Welcome, " + matches[int(inputChar)-1][0])
            matches = []
            print("Begin Typing Next Entry")
        except IndexError:
            pass
