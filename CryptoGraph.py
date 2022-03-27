from Graph import Graph
from Crypto import Crypto

import json
import requests
import time
import copy
from os import listdir
import csv
import sys
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np

class CryptoGraph(Graph):
	def __init__(self):
		super(CryptoGraph, self).__init__()

	def add_tickers(self, tickers):
		for ticker in tickers:
			self.add_node(Crypto(ticker))

	def init_from_price_hist(self, directory = 'Kline'):
		files = listdir(directory)
		csvs = [f'{directory}/{f}' for f in files if f.endswith('csv')]
		for c in csvs:
			with open(c, 'r') as f:
				lines = list(csv.reader(f))[1:]
				d = {float(l[1]):l[2:] for l in lines}
				p = {float(l[1]):float(l[5]) for l in lines}
			self.add_node(Crypto(c.split('/')[-1][:-4], price = p, data = d))
					
	def update_prices(self):
		stub = 'https://api.binance.com/api/v3/ticker/price?symbol='
		nodes = [n for n in self.adj_list.keys()]

		for node in self.adj_list.keys():
			data = requests.get(stub + node.ticker).json()
			node.update_price(int(time.time()), data['price'])

	def calculate_regressions(self, plot_best = False):
		regressions = []
		for i, n1 in enumerate(self.adj_list.keys()):
			for j, n2 in enumerate(self.adj_list.keys()):
				if i <= j:
					continue
				x1 = n1.normalized_price()
				x2 = n2.normalized_price()
				regressions.append((n1, n2, linregress(x1, x2)))
		regressions.sort(reverse = True, key = lambda x: x[2][2])
		if plot_best:
			best = regressions[0]
			x1 = best[0].normalized_price()
			x2 = best[1].normalized_price()
			plt.scatter(x1, x2)
			x = np.linspace(0, 1, 100)
			y = best[2][0]*x + best[2][1]
			plt.plot(x, y)
			plt.show()
		return regressions