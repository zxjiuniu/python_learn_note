#!/usr/bin/env python
#coding: utf-8

import sys,os
import time
import pickle
import getpass

exec_time = time.strftime("%Y-%m-%d %H:%M:%S")

#账单字典
checklist = {
'95588':[],
'95566':[]
}

#银行用户信息(卡号:用户名,密码,额度,余额,欠款,锁)
bank_users={
'95588':['Dave','123456',15000.0,15000.0,0.0,0],
'95566':['Jack','123456',15000.0,15000,0,0.0,0]
}

#商品字典,商品名及价格
products = {
'phone': 3000,
'TV':2500,
'shoes':500,
'clothes':300,
'bike':800
}

#用户登录检查
def check_user():
	print "测试卡号为95588/95566,密码为123456"
	while True:
		global card_num
		pass_try = 3
		card_num = raw_input("请输入您的卡号:")
		if bank_users.has_key(card_num):
			if bank_users[card_num][5] == 1:
				sys.exit("\033[31;1m该卡已经被锁定,请联系管理员解锁\033[0m")	
			while pass_try > 0:
				#card_passwd = raw_input("请输入信用卡密码,还剩%d次:" % pass_try)
				card_passwd = getpass.getpass("请输入信用卡密码,还剩%d次:" % pass_try).strip()
				if card_passwd == bank_users[card_num][1]:
					#print "Welcome:\033[31;1m%s\033[0m,时间:%s" %(bank_users[card_num][0],exec_time)
					break
				else:
					print "\033[31;1m密码不正确,请重新输入\033[0m"		
					pass_try -= 1
					continue
			else:
				bank_users[card_num][5] = 1
				f_write('bank_users.txt',bank_users)
				sys.exit("\033[31;1m密码输错三次,用户已锁定\033[0m")
			
				
			break
		else:
			print "\033[31;1m您输入的卡号不存在,请重新输入\033[0m"
			continue

#显示菜单
def show_menu():
	os.system("clear")
	print "用户:\033[31;1m%s\033[0m,时间:%s" %(bank_users[card_num][0],exec_time)
	print "\033[31;1m\t\t\t\t\t\t    *菜单*\033[0m",
        print '''
		 +------------------------------------------------------------------------------+
                 |\033[32;1m1\033[0m.提现          \t\t\t\t\t\t\033[32;1m4\033[0m.信用卡账单查询|
                 |\033[32;1m2\033[0m.信用卡还款    \t\t\t\t\t\t\033[32;1m5\033[0m.转账汇款      |
                 |\033[32;1m3\033[0m.购买物品      \t\t\t\t\t\t\033[32;1m6\033[0m.退出          |
                 +------------------------------------------------------------------------------+
		 信用卡额度:%d¥ 余额:%d¥ 应还款:%d¥''' % (bank_users[card_num][2],bank_users[card_num][3],bank_users[card_num][4])
	global option
	option = int(raw_input("请选择:"))

#提现
def extract_money():
	while True:
		money = float(raw_input('请输入你要提取金额(手续费为5%):'))
		if money > bank_users[card_num][2]:
			print '提款额度超出了信用卡余额'
			continue
		else:
			bank_users[card_num][3] -= money
			bank_users[card_num][4] += (1+0.05)*money
			print "\033[33;1m本次提取现金:%d¥,手续费为:%d¥\033[0m" %(money,money*0.05)
			ret = raw_input("\033[31;1m是否继续提现(y继续,回车返回主菜单)\033[0m")
			if ret == 'y':
				continue
			else:
				break
			checklist[card_num].append((exec_time,'提现',money,money*0.05))
			f_write('checklist.txt',checklist)
			f_write('bank_users.txt',bank_users)
			break

#还款
def repayment():
	if bank_users[card_num][4] > 0:
		while True:
			repay = raw_input("\033[31;1m请输入你要还款的金额(取消还款q):\033[0m")
			if repay == 'q':
				break
			#elif float(repay) - bank_users[card_num][4] > 0:
			#	print "\033[31;1m还款金额超出欠款,应还款为:%d¥\033[0m" % bank_users[card_num][4]
			#	continue
			else:
				print "\033[31;1m还款成功,本次还款金额为:%d¥\033[0m" % float(repay)
				bank_users[card_num][3] += float(repay)
				#if bank_users[card_num][3] > 15000:
				#	bank_users[card_num][3] = 15000
				bank_users[card_num][4] -= float(repay)
				if bank_users[card_num][4] < 0:
					bank_users[card_num][4] = 0
				checklist[card_num].append((exec_time,'还款',float(repay),0.0))
				f_write('checklist.txt',checklist)
				f_write('bank_users.txt',bank_users)
				ret = raw_input("y继续还款,q返回主菜单:")
				if ret == 'y':
					continue
				else:
					break
	else:
		print("\033[31;1m你的信用良好，没有欠款需要偿还!\033[0m")

#购买
def shopping():
	print "商品列表"
	for k,v in products.items():
		print "%s:%s¥" %(k,v)
	while True:
		buy = raw_input('请输入你要购买的商品(q返回):')
		if bank_users[card_num][3] - products[buy] >= 0:
			bank_users[card_num][3] -= products[buy]
			bank_users[card_num][4] += products[buy]	
			checklist[card_num].append((exec_time,'购买' + buy,products[buy],0.0))
			f_write('checklist.txt',checklist)
			f_write('bank_users.txt',bank_users)
			ret = raw_input("y继续购买,q返回主菜单:")
			if ret == 'y':
				continue
			else:
				break
		elif buy == 'q':
			break
		else:
			print "\033[31;1m你余额不足以购买,请选择购买其他商品"
			continue

#转账功能
def bank_transfer():
	while True:
		rec_card = raw_input("请输入你要转入的卡号(q返回):").strip()
		if bank_users.has_key(rec_card):
			tran_money = int(raw_input("请输入你要转入的金额:"))
			confirm = raw_input("确认你要输入的卡号为:%s,用户名为:%s,转入的金额为:%d(y/n/q)" %(rec_card,bank_users[rec_card][0],tran_money))
			if confirm == 'y':
				bank_users[rec_card][3] += tran_money 
				bank_users[card_num][3] -= tran_money
				checklist[rec_card].append((exec_time,card_num+'转入',tran_money,0.0))
				checklist[card_num].append((exec_time,'转出到'+rec_card,tran_money,0.0))
				f_write('bank_users.txt',bank_users)
				f_write('checklist.txt',checklist)
				print "\033[31;1m转账成功\033[0m"
				ret = raw_input("y继续转账,回车返回主菜单:")
				if ret == 'y':
					continue
				else:
					break
			elif confirm == 'n':
				continue
			else:
				break
		elif rec_card == 'q':
			break
		else:
			print "你输入的账号不存在!"
			continue

#账单查询
def bill_check():
	while True:
		checklist = f_read('checklist.txt')
		print_format = '|  %15s  |    %-13s |  %-7s  |  %-6s  |'
		print '''\t\t\t   \033[31;1m信用卡账单\033[0m
+-----------------------+----------------+-----------+----------+
|  %14s         |  %10s      |   %-8s  |  %-6s  |
+-----------------------+----------------+-----------+----------+''' % ('时间','操作','金额','手续费')
		for i in checklist[card_num]:
			print print_format % i
		ret = raw_input("回车返回主菜单,q退卡:")	
		if ret == 'q':
			sys.exit("Goodbye")
		else:
			break

#定义一个读函数,参数(文件名)
def f_read(filename):
	with open(filename,'rb') as f:
		f_t_v = pickle.load(f)	
		return f_t_v

#定义一个写函数,参数(文件名,要写入的数据)
def f_write(filename,data):
	with open(filename,'wb') as f:
		pickle.dump(data,f)
		f.flush()

#主程序
if __name__ == '__main__':
	#print exec_time
	#checklist.txt文件不存在时创建一个,存在就读取其中的内容
	if os.path.exists('checklist.txt'):
		checklist = f_read('checklist.txt')
	else:
		f_write('checklist.txt',checklist)
	#bank_users.txt文件不存在时创建一个,存在就读取其中的内容
	if os.path.exists('bank_users.txt'):
		bank_users = f_read('bank_users.txt')
	else:
		f_write('bank_users.txt',bank_users)

	#卡解锁
	#bank_users['95588'][5] = 0

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
			bank_transfer()
			continue
		elif option == 6:
			#w_credit_card() #退出之前将信用卡信息写入文件
			#w_checklist()  #退出之前将账单信息写入文件
			sys.exit("\033[31;1m欢迎再次使用信用卡\033[0m")
		else:
			print "请输入正确的编号"
			continue
