# -*- encoding: utf-8 -*-

import requests
import logging
import json
import BaseService
import Utils
from urllib import urlencode
import pandas as pd


class BalanceService(BaseService.BaseService):
	POST_BALANCE = 'balance'
	POST_TRADE_LIST = 'trade_list'
	POST_TRADE_VIEW = 'trade_view'

	def __init__(self):
		super(BalanceService, self).__init__('Balance')
		try:
			f = open('keys.json', 'r')
			conf = json.load(f)
			self.public_key = conf['query']['public_key']
			self.private_key = conf['query']['private_key']
		except Exception as e:
			raise

	def post_balance(self):
		'''
		Account Balance（账户信息）

		列举您的帐户信息

		Path：/api/v1/balance/

		Request类型：POST

		参数

		key - API key

		signature - signature

		nonce - nonce

		返回JSON dictionary

		eth_balance - ETH总余额

		btc_balance - 比特币总余额

		eth_lock - ETH冻结余额

		btc_lock - 比特币冻结余额
		'''
		nonce = Utils.generate_nonce()
		original_params = {'nonce': nonce, 'key': self.public_key}
		params = Utils.reformat_params(original_params, self.private_key)
		url = self.restful_url + BalanceService.POST_BALANCE
		self.logger.info('post_balance: %s, %s' % (url, params))
		response = requests.post(url, data=params)
		return response.json() if response else ''

	def post_trade_list(self, coin, since=0, trade_type='all'):
		'''
		您指定时间后的挂单，可以根据类型查询，比如查看正在挂单和全部挂单
		'''
		nonce = Utils.generate_nonce()
		original_params = {'coin': coin, 'since': since, 'type': trade_type, 'nonce': nonce, 'key': self.public_key}
		params = Utils.reformat_params(original_params, self.private_key)
		url = self.restful_url + BalanceService.POST_TRADE_LIST
		self.logger.info('post_trade_list: %s, %s' % (url, params))
		response = requests.post(url, data=params)
		return response.json() if response else ''

	def post_trade_view(self, coin, trade_id):
		nonce = Utils.generate_nonce()
		original_params = {'coin': coin, 'id': trade_id, 'nonce': nonce, 'key': self.public_key}
		params = Utils.reformat_params(original_params, self.private_key)
		url = self.restful_url + BalanceService.POST_TRADE_VIEW
		self.logger.info('post_trade_view: %s, %s' % (url, params))
		response = requests.post(url, data=params)
		return response.json() if response else ''


if __name__ == '__main__':
	# main()
	pass
