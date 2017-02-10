#!/usr/bin/env python

import sys

stuff = {
'1':{'name':'Jack','sex':'male','age':10,'phone':'113456789'},
'2':{'name':'Tom','sex':'male','age':20,'phone':'123456789'},
'3':{'name':'Lily','sex':'female','age':30,'phone':'133336789'},
'4':{'name':'Rony','sex':'male','age':40,'phone':'143456789'},
'5':{'name':'Steven','sex':'male','age':50,'phone':'153456789'},
'6':{'name':'Jack','sex':'female','age':55,'phone':'163456789'}
}

while True:
	query = raw_input("Please input stuff id number:")

	if query == "quit":
		sys.exit('Goodbye')
	else:
		pass

	for k,v in stuff.items():
		if query == k:
			print k,v
			break
		else:
			for i,j in v.items():
				if query == i or query == j:
					print k,v
					break
				else:
					continue
