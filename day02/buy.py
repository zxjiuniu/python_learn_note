#!/usr/bin/env python

import sys

#Goods list
goods = {
'car':500000,
'phone':5000,
'bike':500,
'tea':50,
'pen':10
}

buylist = []
buylist2 = []

print "\033[31;1mGoods\033[0m:\033[32;1mPrice\033[0m"
for k,v in goods.items():
	print "\033[31;1m%s\033[0m:\033[32;1m%d\033[0m" %(k,v)

salary = int(raw_input("Input your salary:"))

while True:
	#print "If you want to exit,enter quit"
	buy = raw_input("\033[31;1mIf you want to exit,enter quit at anytime.\033[0m\nWhat you want to buy?:")
	if buy == 'quit':
		sys.exit('Goodbye')
	else:
		pass
	if salary >= goods[buy]:
		print "buy succed"
		buylist.append(buy)
		salary -= goods[buy]
		print "\033[32;1mYour shoppinglist:\033[0m"
		print "\033[31;1mGoods\033[0m:\033[32;1mNumbers\033[0m"

		'''
		for i in buylist:
			if i not in buylist2:
				buylist2.append(i)
			else:
				pass
		'''

		for i in set(buylist):
			print "\033[31;1m%s\033[0m:\033[32;1m%d\33[0m" %(i,buylist.count(i))
		print "Your balance is:\033[31;1m%d\033[0m" % salary
		continue
	elif salary >= 10:
		print "\033[31;1mYour can not afford to buy %s\033[0m" % buy 
		print "Your balance is:\033[31;1m%d\033[0m" % salary
		continue
	else:
		sys.exit("\033[31;1mYour are too poor to buy anything.\033[0m") 

