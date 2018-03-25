# -*-coding=utf-8-*-
import datetime
import time, os
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, DateTime, Integer, Text, INT, ForeignKey, Index, Float

import Utils

engine = Utils.get_engine('db_coin')
DBSession = sessionmaker(bind=engine)
Base = declarative_base()


class BtcPrice(Base):
	__tablename__ = 'tb_btcprice'
	date = Column(DateTime, index=True, primary_key=True)
	price = Column(Float)

	def __repr__(self):
		return "Date {}: BTC price: {}".format(self.date, self.price)

Base.metadata.create_all(engine)

def import_data():
	session = DBSession()
	# BTC(date=d, price=p)
	with open('btc_price.csv', 'r') as f:
		content = f.readlines()
	for i in content[1:]:
		# print
		BTC = BtcPrice(date=i.split(',')[0].strip(), price=i.split(',')[1].strip())
		session.add(BTC)

		try:
			session.commit()
		except:
			session.rollback()

	session.close()


def getBtcPrice():
	session = DBSession()
	btc_p_url = 'https://www.coinegg.com/index/pricebtc'
	r = Utils.getWebContent(btc_p_url)
	if not r:
		return None
	price = r.json().get('data').get('cny')
	d, p = (datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), price)
	df = pd.DataFrame({'Datetime': [d], 'Price': [p]}, columns=['Datetime', 'Price'])
	df = df.set_index('Datetime')
	filename = os.path.join(os.path.dirname(__file__), 'btc_price.csv')

	if os.path.exists(filename):
		df.to_csv(filename, mode='a', header=False)
	else:
		df.to_csv(filename, mode='a')

	BTC = BtcPrice(date=d, price=p)
	# BTC(date=d, price=p)
	session.add(BTC)
	try:
		session.commit()
	except:
		session.rollback()

	session.close()

def check_price():
	session=DBSession()
	r=session.query(BtcPrice.price).all()
	for i in r:
		print i[0]

getBtcPrice()
# import_data()
# check_price()