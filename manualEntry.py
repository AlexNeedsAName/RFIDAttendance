#!/usr/bin/env python
import os
import database, forms, getch

configFile = "config.yml"
attendance = forms.form(configFile, "attendance")

clear = "clear"
if(os.name == "nt"): #If Windows
    clear = "cls"

input = ""

#this will be in a loop that is reading input characters
os.system(clear)
print("Manual Entry:\n")
while True:
    inputChar = str(getch.getch())
    os.system(clear)
    print("Manual Entry:\n")
    if(inputChar.isalpha() or ord(inputChar) == 32):
        input+=str(inputChar)
        print(input)
        matches = database.checkForMatches(input)

    elif(ord(inputChar) == 127): #Backspace
        input = input[:-1]
        print(input)
        if(input!=""):
            matches = database.checkForMatches(input)
        else:
            matches = []

    elif(ord(inputChar) == 13): #Enter
	print(input)
	matches = database.checkForMatches(input)

    elif(ord(inputChar) == 3): #Keyboard Interrupt
        break

    elif(inputChar.isdigit()):
        try:
            input = ""
            error = attendance.submit(matches[int(inputChar)-1][1])
            print("Welcome, " + matches[int(inputChar)-1][0])
            matches = []
            print("Begin Typing Next Entry")
        except IndexError:
            pass
