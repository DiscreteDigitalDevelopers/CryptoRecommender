from Graph import Graph
from Crypto import Crypto

import json
import requests
import time
import copy

class CryptoGraph(Graph):
	def __init__(self):
		super(CryptoGraph, self).__init__()

	def add_tickers(self, tickers):
		for ticker in tickers:
			self.add_node(Crypto(ticker))

	def init_from_file(self, filename):
		with open(filename, 'r') as f:
			lines = [i.strip() for i in f.readlines()]
			self.add_tickers(lines)

	def update_prices(self):
		stub = 'https://api.binance.com/api/v3/ticker/price?symbol='
		nodes = [n for n in self.adj_list.keys()]
		for old_node in nodes:
			new_node = copy.deepcopy(old_node)
			data = requests.get(stub + new_node.ticker).json()
			new_node.update_price(int(time.time()), data['price'])
			self.update_node(old_node, new_node)

		# for node in self.adj_list.keys():
		# 	data = requests.get(stub + node.ticker).json()
		# 	node.update_price(int(time.time()), data['price'])
		# 	print('here')