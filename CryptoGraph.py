from Graph import Graph
from Crypto import Crypto
from Edge import Edge

from os import listdir
import csv
import sys
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
from itertools import combinations
import networkx as nx
import json

class CryptoGraph():
	def __init__(self):
		super(CryptoGraph, self).__init__()
		self.G = nx.Graph()

	def make_complete(self):
		for n1, n2 in combinations(self.G.nodes, 2):
			self.G.add_edge(n1, n2)

	def add_tickers(self, tickers):
		for ticker in tickers:
			self.G.add_node(ticker)
		self.make_complete()

	def init_from_price_hist(self, directory = 'Kline/filter'):
		files = listdir(directory)
		csvs = [f'{directory}/{f}' for f in files if f.endswith('csv')]
		for c in csvs:
			with open(c, 'r') as f:
				lines = list(csv.reader(f))[1:]
				d = {int(l[1]):l[2:] for l in lines}
				p = {int(l[1]):float(l[5]) for l in lines}
			node = c.split('/')[-1][:-4]
			self.G.add_node(node)
			self.G.nodes[node]['price'] = p
			self.G.nodes[node]['data'] = d
		self.make_complete()

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

	@staticmethod
	def normalize_price(price):
		y = np.array([i for i in price.values()])
		y /= np.max(y)
		return y

	def calculate_regressions(self, plot_best = False):
		for n1, n2 in combinations(self.G.nodes, 2):
			p1 = self.normalize_price(self.G.nodes[n1]['price'])
			p2 = self.normalize_price(self.G.nodes[n2]['price'])
			self.G.edges[n1, n2]['r2'] = linregress(p1, p2)[2]**2

	def get_kmeans_clusters(self, fname = 'scraped/categories.json'):
		with open(fname) as f:
			dat = json.load(f)
			for n in self.G.nodes:
				for d in dat:
					if n == f'{d["symbol"]}USDT':
						self.G.nodes[n]['kmeans_cat'] = d['meta']
						break

	def get_dbscan_clusters(self, fname = 'scraped/dbscan_categories.json'):
		with open(fname) as f:
			dat = json.load(f)
			for n in self.G.nodes:
				for d in dat:
					if n == f'{d["symbol"]}USDT':
						self.G.nodes[n]['dbscan_cat'] = d['meta']
						break


		# if plot_best:
		# 	best = regressions[0]
		# 	x1 = best[0].normalized_price()
		# 	x2 = best[1].normalized_price()
		# 	plt.scatter(x1, x2, s = 4)
		# 	plt.xlabel(f'{best[0].ticker}')
		# 	plt.ylabel(f'{best[1].ticker}')
		# 	plt.title(f'Best Regression - R^2 = {best[2][2]**2:.4f}')
		# 	x = np.linspace(0, 1, 100)
		# 	y = best[2][0]*x + best[2][1]
		# 	plt.plot(x, y)
		# 	plt.savefig('Images/best_reg.png', dpi = 500)
		# return regressions