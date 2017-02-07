#!/usr/bin/env python

#use key to save username and password
user = {
'dave':'123456'}

#accept input
def user_input():
	global name,password
	name = raw_input('Username:')
	password = raw_input('Password:')


#try three times
counter = 0
while  counter < 3:
	user_input()
	if name in user.keys() and password == user[name]:
		print "Welcome to use python"		
		break
	else:
		print "Username or password is not correct,try again."
		counter += 1
else:
	print "User as locked"
