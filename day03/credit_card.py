#!/usr/bin/env python
#coding: utf-8

import sys,os
import time
import pickle

exec_time = time.strftime("%Y-%m-%d %H:%M:%S")

#0表示用户不锁定,3表示用户密码尝试次数
user_lock = [0,3]

#列表存三个数，分别为信用卡额度、余额、还款数
limit = [15000.00,15000.00,0.00]

#账单字典
checklist = []

#银行用户信息
bank_users={
'95588':('Dave','123456'),
'95566':('Jack','123456')
}


#商品字典,商品名及价格
products = {
'phone': 3000,
'TV':2500,
'shoes':500,
'clothes':300,
'bike':800
}


#确认用户信息
def check_user():
	print "测试卡号为95588/95566,密码为123456"
	while True:
		card_num = raw_input("请输入您的卡号:")
		if user_lock[0] == 1:
			sys.exit("\033[31;1m卡已经被锁定,请联系管理员解锁\033[0m")	
		if bank_users.has_key(card_num):
			while user_lock[1] > 0:
				card_passwd = raw_input("请输入信用卡密码,还剩%d次:" % user_lock[1])
				if card_passwd == bank_users[card_num][1]:
					print "Welcome:\033[31;1m%s\033[0m,时间:%s" %(bank_users[card_num][0],exec_time)
					break
				else:
					print "\033[31;1m密码不正确,请重新输入\033[0m"		
					user_lock[1] -= 1
					continue
			else:
				user_lock[0] = 1
				w_write('user_lock.txt',user_lock)
				sys.exit("\033[31;1m密码输错三次,用户已锁定\033[0m")
			
				
			break
		else:
			print "\033[31;1m您输入的卡号不存在,请重新输入\033[0m"
			continue
	pass

#显示菜单
def show_menu():
	print "\033[31;1m\t\t\t\t\t\t    *菜单*\033[0m",
        print '''
		 +------------------------------------------------------------------------------+
                 |\033[32;1m1\033[0m.提现          \t\t\t\t\t\t\033[32;1m4\033[0m.信用卡账单查询|
                 |\033[32;1m2\033[0m.信用卡还款    \t\t\t\t\t\t\033[32;1m5\033[0m.转账汇款      |
                 |\033[32;1m3\033[0m.购买物品      \t\t\t\t\t\t\033[32;1m6\033[0m.退出          |
                 +------------------------------------------------------------------------------+
		 信用卡额度:%d¥ 余额:%d¥ 应还款:%d¥''' % (limit[0],limit[1],limit[2])
	
	global option
	option = int(raw_input("请选择:"))

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
			print "\033[33;1m本次提取现金:%d¥,手续费为:%d¥\033[0m" %(money,money*0.05)
			checklist.append((exec_time,'提现',money,money*0.05))
			w_write('checklist.txt',checklist)
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
				w_write('checklist.txt',checklist)
				w_write('credit_card.txt',limit)
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
		w_write('credit_card.txt',limit)
		w_write('checklist.txt',checklist)
	else:
		print "\033[31;1m你的信用卡余额不足"
			
	pass

#账单查询
def bill_check():
	checklist = r_read('checklist.txt')
	print_format = '|  %15s  |    %-13s |  %-7s  |  %-6s  |'
	print '''\t\t\t   \033[31;1m信用卡账单\033[0m
+-----------------------+----------------+-----------+----------+
|  %14s         |  %10s      |   %-8s  |  %-6s  |
+-----------------------+----------------+-----------+----------+''' % ('时间','操作','金额','手续费')
	for i in checklist:
		print print_format % i
	pass

#定义一个读函数,参数(文件名)
def r_read(filename):
	with open(filename,'rb') as f:
		f_t_v = pickle.load(f)	
		return f_t_v

#定义一个写函数,参数(文件名,要写入的数据)
def w_write(filename,data):
	with open(filename,'wb') as f:
		pickle.dump(data,f)
		f.flush()

#主程序
if __name__ == '__main__':
	#print exec_time
	#credit_card.txt文件不存在时创建一个,存在就读取其中的内容
	if os.path.exists('credit_card.txt'):
		limit = r_read('credit_card.txt')
	else:
		w_write('credit_card.txt',limit)
	#checklist.txt文件不存在时创建一个,存在就读取其中的内容
	if os.path.exists('checklist.txt'):
		checklist = r_read('checklist.txt')
	else:
		w_write('checklist.txt',checklist)
	#bank_users.txt文件不存在时创建一个,存在就读取其中的内容
	if os.path.exists('bank_users.txt'):
		bank_users = r_read('bank_users.txt')
	else:
		w_write('bank_users.txt',bank_users)
	#user_lock.txt文件不存在时创建一个,存在就读取其中的内容
	if os.path.exists('user_lock.txt'):
		user_lock = r_read('user_lock.txt')
	else:
		w_write('user_lock.txt',user_lock)

	check_user()

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
			continue
		elif option == 6:
			#w_credit_card() #退出之前将信用卡信息写入文件
			#w_checklist()  #退出之前将账单信息写入文件
			sys.exit("\033[31;1m欢迎再次使用信用卡\033[0m")
			
		else:
			print "请输入正确的编号"
			continue
