# -*-coding=utf-8-*-
import datetime
import time,os
import pandas as pd

from coinegg import Utils

def getBtcPrice():
    btc_p_url = 'https://www.coinegg.com/index/pricebtc'
    r=Utils.getWebContent(btc_p_url)
    price = r.json().get('data').get('cny')
    d,p= (datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), price)
    df=pd.DataFrame({'Datetime':[d],'Price':[p]},columns=['Datetime','Price'])
    df=df.set_index('Datetime')
    filename='btc_price.csv'
    if os.path.exists(filename):
        df.to_csv('btc_price.csv',mode='a',header=False)
    else:
        df.to_csv('btc_price.csv',mode='a')


getBtcPrice()