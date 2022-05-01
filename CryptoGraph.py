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

	def init_from_price_hist(self, directory = 'Kline/coins'):
		files = listdir(directory)
		csvs = [f'{directory}/{f}' for f in files if f.endswith('csv')]
		for c in csvs:
			with open(c, 'r') as f:
				lines = list(csv.reader(f))[1:]
				if len(lines) < 1000:
					continue
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
				found = False
				for d in dat:
					if n == f'{d["symbol"]}USDT':
						self.G.nodes[n]['kmeans_cat'] = d['meta']
						found = True
						break
				if not found:
					self.G.nodes[n]['kmeans_cat'] = -1

	def get_dbscan_clusters(self, fname = 'scraped/dbscan_categories.json'):
		with open(fname) as f:
			dat = json.load(f)
			for n in self.G.nodes:
				found = False
				for d in dat:
					if n == f'{d["symbol"]}USDT':
						self.G.nodes[n]['dbscan_cat'] = d['meta']
						found = True
						break
				if not found:
					self.G.nodes[n]['dbscan_cat'] = -1

	def aggregate_metrics(self, r_weight = 0.8, k_weight = 0.3, d_weight = 0.3):
		max_agg = 0
		for n1, n2 in self.G.edges:
			same_kmeans = self.G.nodes[n1]['kmeans_cat'] == self.G.nodes[n2]['kmeans_cat']
			same_dbscan = self.G.nodes[n1]['dbscan_cat'] == self.G.nodes[n2]['dbscan_cat']
			w = r_weight * self.G.edges[n1, n2]['r2'] + k_weight * same_kmeans + d_weight * same_dbscan
			self.G.edges[n1, n2]['aggregate'] = w
			if w > max_agg:
				max_agg = w

		for n1, n2 in self.G.edges:
			self.G.edges[n1, n2]['aggregate'] /= max_agg

	def get_similar_cryptos(self, ticker):
		sim = []
		for n in self.G.neighbors(ticker):
			sim.append((n, self.G.edges[ticker, n]['aggregate']))
		sim.sort(key = lambda x: x[1], reverse = True)
		return sim