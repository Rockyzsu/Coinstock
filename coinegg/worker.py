# *-*coding:utf-8-*-
import BalanceService
import pandas as pd
import Utils, re
import itchat, time
from itchat.content import *

DB_NAME='db_coin'
loggers=Utils.logger('coinegg.log')


def store_data():
	coin_name = 'zet'
	balanceService = BalanceService.BalanceService()
	db = Utils.mongo("coin")
	collection = db[coin_name]
	# balance = balanceService.post_balance()
	# print balance
	trade_list = balanceService.post_trade_list(coin_name, 0, 'all')
	# df = pd.DataFrame()
	trade_list = dict(trade_list)

	date = []
	ex_type = []
	status = []
	price = []
	amount_original = []

	# date=[]
	# date=[]
	# date=[]
	# date=[]
	# print trade_list
	collection.remove()

	for trade in trade_list.get('data'):
		collection.insert(trade)


# 	print trade

# if trade.get('status')=='closed':
# print "datetime: {} ".format(trade.get('datetime')),
# print "type: {} ".format(trade.get('type')),
# print "status: {} ".format(trade.get('status')),
# print "price: {} ".format(trade.get('price')),
# print "amount_original: {} ".format(trade.get('amount_original'))


# trade_view = balanceService.post_trade_view('doge', 6860502)
# print trade_view

# print df
def analysis():
	db = Utils.mongo("coin")
	coin_name = 'zet'

	collection = db[coin_name]
	total = []
	for item in collection.find({'status': 'closed'}):
		# print type(item)
		# print item
		price = float(item.get('price'))
		if item.get('type') == u'sell':
			price = -1.0 * price
		amount_original = float(item.get('amount_original'))
		total.append(amount_original * price)
	print total
	print sum(total)


# @itchat.msg_register([TEXT])
def wechat_monitor(content):
	user = Utils.js.get('wechat_user')
	# print user
	account = itchat.get_friends(u'wei')
	# print 'acount {}'.format(account)
	# print type(account)
	for i in account:
		# print type(i)
		# print i
		if i[u'PYQuanPin'] == u'wei':
			username = i['UserName']
		# print username
	# print i
	# itchat.send(content, toUserName=id)

	# print 'done'
	itchat.send((str(content)), toUserName=username)


'''
监测市场的行情
'''


def detect_market(focus_list=[]):
	ret_coin_info = Utils.coinegg_coins()
	# print 'dfafffa'
	if not ret_coin_info:
		loggers.info(u'Failed to get coinegg web content, retry')
		return None
	# print ret_coin_info
	resullt=dict()
	red=0
	counts=0
	for coin,detail in ret_coin_info.items():
		# print coin,'\t',detail[8]
		if detail[8]>0:
			red+=1
		counts+=1
		resullt[coin]=detail[8]
		# print coin,detail[8]
		if detail[8]>20:
			wechat_monitor(u'coin {} is rasing to {}, go to focus!'.format(coin,detail[8]))
			loggers.info(u'coin {} is rasing to {}, go to focus!'.format(coin,detail[8]))


	# print max(resullt.values())
	# lens=len(resullt)
	# wechat_monitor(red/(1.0*counts)*100)
	if red / (1.0 * counts) * 100 >= 30:
		# print "Hot !!!"

		loggers.info(u'ICO is hotting, more than {} coin percentage is red go to focus!'.format(red/(1.0*counts)*100))
		wechat_monitor(u'ICO is hotting, more than {} coin percentage is red go to focus!'.format(red/(1.0*counts)*100))


	if focus_list:
		for coin in focus_list:

			if resullt[coin] >10:
				wechat_monitor(u'Coin {} is rasing as {}'.format(coin,resullt[coin]))
				loggers.info(u'Coin {} is rasing as {}'.format(coin,resullt[coin]))


def main():
	MINUTES=60
	coin_list=['zet','ifc','mryc']
	# loggers.info('asdfb')
	# print "fdafdafa"
			if resullt[coin] > 10:
				wechat_monitor(u'Coin {} is rasing as {}'.format(coin, resullt[coin]))



	while 1:
	# 	# store_data()
	# 	# analysis()

		detect_market(coin_list)

		# print 'dafafdaf'
		loggers.info('Go to next 30mins')
		time.sleep(30*MINUTES)
		# itchat.auto_login()


if __name__ == '__main__':
	itchat.auto_login(hotReload=True)
	# itchat.run()
	print 'go to main'
	main()
