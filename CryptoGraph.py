from Graph import Graph
from Crypto import Crypto
from Edge import Edge

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

	def init_from_price_hist(self, directory = 'Kline/filter'):
		files = listdir(directory)
		csvs = [f'{directory}/{f}' for f in files if f.endswith('csv')]
		for c in csvs:
			with open(c, 'r') as f:
				lines = list(csv.reader(f))[1:]
				d = {int(l[1]):l[2:] for l in lines}
				p = {int(l[1]):float(l[5]) for l in lines}
			self.add_node(Crypto(c.split('/')[-1][:-4], price = p, data = d, last_price = (int(lines[-1][1]), float(lines[-1][5]))))
					
	def update_prices(self):
		stub = 'https://api.binance.com/api/v3/ticker/price?symbol='
		nodes = [n for n in self.adj_list.keys()]

		for node in self.adj_list.keys():
			data = requests.get(stub + node.ticker).json()
			node.update_price(int(time.time()), data['price'])

	def import_correlation_data(self, filename = 'graph_data/cor_close_vol.csv'):
		lpp = 970
		with open(filename, 'r') as f:
			lines = list(csv.reader(f))[1:]
			for p in range(len(lines)//lpp):
				pair_data = {int(lines[x][2]):(float(lines[x][3]), float(lines[x][4])) for x in range(p*lpp, (p+1)*lpp)}
				t1 = lines[p*lpp][0]
				t2 = lines[p*lpp][1]
				edge = self.get_edge(t1, t2)[1]
				edge.pair_data = pair_data

	def calculate_regressions(self, plot_best = False):
		regressions = []
		for i, n1 in enumerate(self.adj_list.keys()):
			for j, n2 in enumerate(self.adj_list.keys()):
				if i <= j:
					continue
				x1 = n1.normalized_price()
				x2 = n2.normalized_price()
				regressions.append((n1, n2, linregress(x1, x2)))
				self.add_edge(n1, n2, Edge(regression_weight = regressions[-1][2][2]), undirected = True)
		regressions.sort(reverse = True, key = lambda x: x[2][2])
		if plot_best:
			best = regressions[0]
			x1 = best[0].normalized_price()
			x2 = best[1].normalized_price()
			plt.scatter(x1, x2, s = 4)
			plt.xlabel(f'{best[0].ticker}')
			plt.ylabel(f'{best[1].ticker}')
			plt.title(f'Best Regression - R^2 = {best[2][2]**2:.4f}')
			x = np.linspace(0, 1, 100)
			y = best[2][0]*x + best[2][1]
			plt.plot(x, y)
			plt.savefig('Images/best_reg.png', dpi = 500)
		return regressions