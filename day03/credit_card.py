#!/usr/bin/env python
#coding: utf-8

import sys,os
import time
import pickle

exec_time = time.strftime("%Y-%m-%d %H:%M:%S")

#列表存三个数，分别为信用卡额度、余额、还款数
limit = [15000.00,15000.00,0.00]

#账单字典
checklist = []

#商品字典,商品名及价格
products = {
'phone': 3000,
'TV':2500,
'shoes':500,
'clothes':300,
'bike':800
}


#显示菜单
def show_menu():
	print "\033[32;1m你的信用卡额度为:%d¥\033[0m" % limit[0]
	print "\033[32;1m你的信用卡余额为:%d¥ 应还款为:%d¥\033[0m" % (limit[1],limit[2])
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
	#global limit
	while True:
		money = float(raw_input('请输入你要提取金额(手续费为5%):'))
		if money > limit[1]:
			print '提款额度超出了信用卡余额'
			continue
		else:
			limit[1] = limit[1] - money
			limit[2] += (1+0.05)*money
			print "\033[33;1m你已成功提取现金:%d¥,手续费为:%d¥\033[0m" %(money,money*0.05)
			checklist.append((exec_time,'提现',money,money*0.05))
			w_checklist()
			break
	pass

#还款
def repayment():
	if limit[2] > 0:
		while True:
			repay = raw_input("\033[31;1m请输入你要还款的金额(取消还款q):\033[0m")
			if repay == 'q':
				break
			elif float(repay) - limit[2] > 0:
				print "\033[31;1m还款金额超出欠款,应还款为:%d¥\033[0m" % limit[2]
				continue
			else:
				print "\033[31;1m还款成功,本次还款金额为:%d¥\033[0m" % float(repay)
				limit[1] += float(repay)
				if limit[1] > 15000:
					limit[1] = 15000
				limit[2] -= float(repay)
				checklist.append((exec_time,'还款',float(repay),0.0))
				w_checklist()
				break
	else:
		print("\033[31;1m你的信用良好，没有欠款需要偿还!\033[0m")
	pass

#购买
def shopping():
	print "商品列表"
	for k,v in products.items():
		print "%s:%s¥" %(k,v)
	buy = raw_input('请输入你要购买的商品:')
	if limit[1] - products[buy] >= 0:
		limit[1] -= products[buy]
		limit[2] += products[buy]	
		checklist.append((exec_time,'购买' + buy,products[buy],0.0))
		w_credit_card()
		w_checklist()
	else:
		print "\033[31;1m你的信用卡余额不足"
			
	pass

#账单查询
def bill_check():
	r_checklist()	
	print '''\t\t\033[31;1m信用卡账单
|%-21s|操作|%-9s|手续费|\033[0m''' % ('时间','金额')
	for i in checklist:
		print '|%s|%s|%-7s|%-6s|' % i
	pass

#读credit_card.txt文件
def r_credit_card():
	with open('credit_card.txt','rb') as f:
		global limit
		limit = pickle.load(f)	

#写credit_card.txt文件
def w_credit_card():
	with open('credit_card.txt','wb') as f:
		pickle.dump(limit,f)	
#读checklist.txt文件
def r_checklist():
	with open('checklist.txt','rb') as f:
		global checklist
		checklist = pickle.load(f)	

#写checklist.txt文件
def w_checklist():
	with open('checklist.txt','wb') as f:
		pickle.dump(checklist,f)	

#主程序
if __name__ == '__main__':
	print exec_time
	#credit_card.txt文件不存在时创建一个,存在就读取其中的内容
	if os.path.exists('credit_card.txt'):
		r_credit_card()
	else:
		w_credit_card()
	#checklist.txt文件不存在时创建一个,存在就读取其中的内容
	if os.path.exists('checklist.txt'):
		r_checklist()
	else:
		w_checklist()
	while True:
		try:
			show_menu()
		except ValueError:
			print "\033[31;1m请输入数字\033[0m"
			continue
		
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
			w_credit_card() #退出之前将信用卡信息写入文件
			w_checklist()  #退出之前将账单信息写入文件
			sys.exit("\033[31;1m欢迎再次使用信用卡\033[0m")
			
		else:
			print "请输入正确的编号"
			continue
