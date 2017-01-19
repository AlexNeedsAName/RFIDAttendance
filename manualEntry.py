#!/usr/bin/env python
import os
import database, forms, getch

configFile = "config.yml"
attendance = forms.form(configFile, "attendance")

clear = "clear"
backspace = 127
enter = 13
interrupt = 3
space = 32
if(os.name == "nt"): #If Windows
    clear = "cls"
    backspace = 8

input = ""

#this will be in a loop that is reading input characters
os.system(clear)
print("Manual Entry:\n")
while True:
    inputChar = str(getch.getch())
    os.system(clear)
    print("Manual Entry:\n")
    if(inputChar.isalpha() or ord(inputChar) == space):
        input+=str(inputChar)
        print(input)
        matches = database.checkForMatches(input)

    elif(ord(inputChar) == backspace): #Backspace
        input = input[:-1]
        print(input)
        if(input!=""):
            matches = database.checkForMatches(input)
        else:
            matches = []

    elif(ord(inputChar) == enter): #Enter
	print(input)
	matches = database.checkForMatches(input)

    elif(ord(inputChar) == interrupt): #Keyboard Interrupt
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
