#-*-coding=utf-8-*-
import requests,datetime
from lxml import etree
import pandas as pd
from sqlalchemy import create_engine
import random,time
engine=create_engine('mysql+pymysql://root:@localhost:3306/coins?charset=utf8')

user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.120 Chrome/37.0.2062.120 Safari/537.36'
headers={'User-Agent':user_agent}

def getWebContent(url):
	# url=url.format(kind)
	r=requests.get(url,headers=headers)
	
	if r.status_code==200:
		return r.text
	else:
		return None

def getCoinList():
	content=getWebContent(url='https://coinmarketcap.com/tokens/views/all/'
)
	tree=etree.HTML(content)
	# table=tree.xpath()
	# if not table:
	# 	reutrn None
	df=pd.DataFrame()

	# for coin in table:
	df['currency-symbol']=tree.xpath('//tbody/tr//span[@class="currency-symbol"]/a/text()')	
	df['currency-name']=tree.xpath('//tbody/tr//a[@class="currency-name-container"]/text()')
	df['platformsymbol']=tree.xpath('//tbody/tr/@data-platformsymbol')
	df['platform-name']=tree.xpath('//tbody/tr//td[@class="no-wrap platform-name"]/a/text()')

	df['price(->bct)']=tree.xpath('//tbody/tr//td[@class="no-wrap text-right"]/a/@data-btc')
	df['datetime']=datetime.datetime.now()
	return df

def datastore():
	df=getCoinList()
	df.to_sql('tokens',engine)



def getBtcPrice():
	btc_p_url='https://www.coinegg.com/index/pricebtc'
	try:
		r=requests.get(url=btc_p_url,headers=headers)
	except Exception,e:
		print e
		return None

	return r.json().get('data').get('cny')


def coinegg_coins():
	url='https://www.coinegg.com/coin/btc/allcoin?t={}'.format(random.random())
	print url
	retry=3
	for _ in range(retry):
		text=getWebContent(url)
		if not text:
			continue
		time.sleep(random.random())

	if not text:
		print 'failed to get web content'
		return None

	return map(lambda x:x.upper(),eval(text).keys())

def find_fake():
	df=getCoinList()
	coinegglist=set(coinegg_coins())
	# print coinegglist
	fakecoin=set(df['currency-symbol'].values)
	print coinegglist & fakecoin
def main():
	# datastore()
	print	getBtcPrice()
	# coinegg_coins()
	# find_fake()

if __name__ == '__main__':
	main()