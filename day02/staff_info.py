#!/usr/bin/env python

import sys

stuff = {
'1':{'name':'Jack','sex':'male','age':10,'phone':'113456789'},
'2':{'name':'Tom','sex':'male','age':20,'phone':'123456789'},
'3':{'name':'Lily','sex':'female','age':30,'phone':'133336789'},
'4':{'name':'Rony','sex':'male','age':40,'phone':'143456789'},
'5':{'name':'Steven','sex':'male','age':50,'phone':'153456789'}
}

while True:
	id = raw_input("Please input stuff id number:")

	if id == "quit":
		sys.exit('Goodbye')
	else:
		pass

	if stuff.has_key(id):
		print "id:%s name:%s sex:%s age:%d phone:%s" %(id,stuff[id]['name'],stuff[id]['sex'],stuff[id]['age'],stuff[id]['phone'])
	else:
		print "The stuff id is not exist"
		continue
