#!/usr/bin/env python

import sys

#use key to save username and password
user = {
'dave':'123456'}

#accept input
def user_input():
	global name,password
	while True:
		name = raw_input('Username:').strip()
		if len(name) == 0:
			print "\033[31;1mUsername can not be null\033[0m"
			continue
		else:
			break
	while True:
		password = raw_input('Password:').strip()
		if len(password) == 0:
			print "\033[31;1mPassword can not be null\033[0m"
			continue
		else:
			break

#Have three chances to try
counter = 0
while  counter < 3:
	print "You have %s chances to try to login" %(3-counter)
	user_input()
	if name in user.keys() and password == user[name]:
		#print "Welcome to use python"		
		#break
		sys.exit("\033[32;1mWelcome to use python\033[0m")
	else:
		print "Username or password is not correct,try again."
		counter += 1
else:
	print "\033[31;1mYou have more than attemps,user has locked\033[0m"
