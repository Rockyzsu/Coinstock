# -*- encoding: utf-8 -*-
from lxml import etree
import pandas as pd
import requests
import hashlib
import hmac, random
import time, datetime
from collections import OrderedDict
from urllib import urlencode
import json
from sqlalchemy import create_engine
import pymongo
<<<<<<< HEAD
import os,logging
=======
import os

>>>>>>> origin/master
# Nonce Length
JUBI_NONCE_LENGHT = 12
user_agent = 'user-agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
headers = {'User-Agent': user_agent}
key_file = os.path.join(os.path.dirname(__file__), 'keys.json')
with open(key_file) as f:
	js = json.load(f)


def getMd5Hash(s):
	m = hashlib.md5()
	m.update(s)
	return m.hexdigest()


def generate_nonce_from_timestamp():
	current_timestamp = time.time() * 1000
	return str(long(current_timestamp))


generate_nonce = generate_nonce_from_timestamp


def generate_signature(msg, private_key):
	msg = bytes(msg).encode('utf-8')
	k = bytes(getMd5Hash(private_key)).encode('utf-8')
	signature = hmac.new(k, msg, digestmod=hashlib.sha256).hexdigest()
	return signature


def reformat_params(params, private_key):
	orderDict = OrderedDict(params)
	param_str = urlencode(orderDict)  # '&'.join(['%s=%s' % (str(k), str(v)) for (k, v) in orderDict.items()])
	signature = generate_signature(param_str, private_key)
	orderDict['signature'] = signature
	return orderDict


def get_engine(db_name):
	user = js.get('MYSQL').get('USER')
	password = js.get('MYSQL').get('PASSWORD')
	host = js.get('MYSQL').get('HOST')
	engine = create_engine('mysql+pymysql://{}:{}@{}:3306/{}?charset=utf8'.format(user, password, host, db_name))
	return engine


def mongo(db_name):
	host = js.get('MONGO').get('HOST')
	port = js.get('MONGO').get('PORT')
	client = pymongo.MongoClient(host, port)
	return client[db_name]


def getWebContent(url, retry=5):
	if retry > 0:
		try:
			r = requests.get(url, headers=headers)
			if r.status_code == 200:
				return r
		except Exception, e:
			print 'retry {}'.format(retry)
			getWebContent(url, retry - 1)
	else:
		return None


def coinegg_coins():
	url = 'https://www.coinegg.com/coin/btc/allcoin?t={}'.format(random.random())
	text = getWebContent(url).text
	# print 'ddfa'
	if not text:
		print 'failed to get web content'
		return None
	return eval(text)


# return map(lambda x: x.upper(), eval(text).keys())


def getCoinList():
	content = getWebContent(url='https://coinmarketcap.com/tokens/views/all/'
							)
	tree = etree.HTML(content)
	# table=tree.xpath()
	# if not table:
	# 	reutrn None
	df = pd.DataFrame()

	# for coin in table:
	df['currency-symbol'] = tree.xpath('//tbody/tr//span[@class="currency-symbol"]/a/text()')
	df['currency-name'] = tree.xpath('//tbody/tr//a[@class="currency-name-container"]/text()')
	df['platformsymbol'] = tree.xpath('//tbody/tr/@data-platformsymbol')
	df['platform-name'] = tree.xpath('//tbody/tr//td[@class="no-wrap platform-name"]/a/text()')

	df['price(->bct)'] = tree.xpath('//tbody/tr//td[@class="no-wrap text-right"]/a/@data-btc')
	df['datetime'] = datetime.datetime.now()
	return df

def logger(filename):
	file=os.path.join(os.path.dirname(__file__),filename)
	mylogger =logging.getLogger('mylogger')
	mylogger.setLevel(logging.DEBUG)

	f_handler = logging.FileHandler(file)
	f_handler.setLevel(logging.DEBUG)
	formatter = logging.Formatter('[%(asctime)s][%(filename)s][%(levelname)s]::: %(message)s')

	f_handler.setFormatter(formatter)	
	mylogger.addHandler(f_handler)
	return mylogger

if __name__ == '__main__':
	# get_engine('db_coint')
	# pass
	# coinegg_coins()

	btc_p_url = 'https://www.coinegg.com/index/pricebtc'
	print getWebContent(btc_p_url, 3)
