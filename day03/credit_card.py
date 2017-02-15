#!/usr/bin/env python
#coding: utf-8

import sys

limit = 15000

products = {
'phone': 3000,
'TV':2500,
'shoes':500,
'clothes':300,
'bike':800
}


#显示菜单
def show_menu():
	print "\033[31;1m你的信用卡额度为:%d\033[0m" % limit
	print '''\033[32;1m\t\t信用卡菜单：
		1、提现。
		2、信用卡还款。
		3、购买物品。
		4、信用卡账单查询。
		5、退出。\033[0m'''
	global option
	option = int(raw_input("\033[32;1m请选择你要进行的操作:\033[0m"))

#提现
def extract_money():
	global limit
	while True:
		money = int(raw_input('请输入你要提取金额(手续费为5%):'))
		if money > 15000:
			print '提款额度超出了信用卡可用额度'
			continue
		else:
			limit -= money
			print "\033[33;1m你已成功提取现金:%d,手续费为:%d\033[0m" %(money,money*0.05)
			break
	
	
	pass

#还款
def repayment():
	print "还款"
	pass

#购买
def shopping():
	print "购买"
	pass

#账单查询
def bill_check():
	print "账单查询"
	pass

#主程序
if __name__ == '__main__':
	
	while True:
		show_menu()
		if option == 1:
			extract_money()
			continue
		elif option == 2:
			repayment()
			continue
		elif option == 3:
			shopping()
			continue
		elif option == 4:
			bill_check()
			continue
		elif option == 5:
			sys.exit("\033[31;1m欢迎再次使用信用卡\033[0m")
			
		else:
			print "请输入正确的编号"
			continue
