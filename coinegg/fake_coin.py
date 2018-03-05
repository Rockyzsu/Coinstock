# -*-coding=utf-8-*-
import datetime
import random
import time,os

import pandas as pd
import requests
from lxml import etree
from sqlalchemy import create_engine
from coinegg import Utils
engine = create_engine('mysql+pymysql://root:@localhost:3306/coins?charset=utf8')


def getCoinList():
    content = Utils.getWebContent(url='https://coinmarketcap.com/tokens/views/all/'
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


def datastore():
    df = getCoinList()
    df.to_sql('tokens', engine)





def coinegg_coins():
    url = 'https://www.coinegg.com/coin/btc/allcoin?t={}'.format(random.random())
    print url
    retry = 3
    for _ in range(retry):
        text = Utils.getWebContent(url)
        if not text:
            continue
        time.sleep(random.random())

    if not text:
        print 'failed to get web content'
        return None

    return map(lambda x: x.upper(), eval(text).keys())


def find_fake():
    df = getCoinList()
    coinegglist = set(coinegg_coins())
    # print coinegglist
    fakecoin = set(df['currency-symbol'].values)
    print coinegglist & fakecoin


def main():
    # datastore()
    # print    getBtcPrice()
    store_data()

    # coinegg_coins()
    # find_fake()

if __name__ == '__main__':
    main()
