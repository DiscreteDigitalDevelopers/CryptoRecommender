'''
This script visualizes time series correlation data between cryptos
'''
import numpy as np
import csv
import os
from matplotlib import pyplot as plt
import talib
import networkx as nx
from tqdm import tqdm
import sys


def readVolPrice(filename):
	# read csv
	close_prices = []
	close_vols = []
	with open(f'./Kline/filter/{filename}.csv', 'r', encoding='utf-8') as f:
		reader = csv.reader(f)
		next(reader) # ignore header
		for row in reader:
			close_prices.append(float(row[-1]))
			close_vols.append(float(row[-2]))
	close_prices = np.array(close_prices) / np.max(close_prices)
	close_vols = np.array(close_vols) / np.max(close_vols)
	return close_prices, close_vols

if __name__ == '__main__':
	
	# # read all csv
	# p_data = {}
	# v_data = {}
	# cryptos = set()
	# name2idx = {}
	# idx2name = {}
	# for idx, fname in enumerate(os.listdir('./Kline/filter/')):
	# 	fname = fname.split('.')[0]
	# 	p_data[fname[:-4]], v_data[fname[:-4]] = readVolPrice(fname)
	# 	cryptos.add(fname[:-4])
	# 	name2idx[fname[:-4]] = idx
	# 	idx2name[idx] = fname[:-4]

	# # print(p_data)
	# # print(v_data)

	# print(name2idx)

	# # compute correlation and form adjacency matrix
	# L = len(name2idx)
	# tp = 200
	# adj_mat = np.zeros((1000, L, L)) # time x L x L, bot half is price, top half is vol
	# for i in range(L):
	# 	for j in range(i + 1, L):
	# 		i_name = idx2name[i]
	# 		j_name = idx2name[j]
	# 		i_p, i_v = p_data[i_name], v_data[i_name]
	# 		j_p, j_v = p_data[j_name], v_data[j_name]
	# 		cor_p = talib.CORREL(i_p, j_p, timeperiod=tp)
	# 		cor_v = talib.CORREL(i_v, j_v, timeperiod=tp)
	# 		adj_mat[:, i, j] = cor_p
	# 		adj_mat[:, j, i] = cor_v

	# adj_mat = adj_mat[tp:]

	# np.save('adj_mat.npy', adj_mat)

	# print(adj_mat[0])
	# print(adj_mat[100])
	# print(adj_mat[500])

	# create Graph
	G = nx.complete_graph(L)
	for e in G.edges.data():
		e[2]['price'] = adj_mat[:, e[0], e[1]]
		e[2]['volume'] = adj_mat[:, e[1], e[0]]

	# visualize 
	pos = nx.spring_layout(G, seed=69)
	for i in tqdm(range(1000 - tp)):
		edges, weights = zip(*nx.get_edge_attributes(G,'price').items())
		weights = [w[i] for w in weights]
		nx.draw(G, pos=pos, edgelist=edges, edge_color=weights, edge_cmap=plt.cm.cool, with_labels=True)
		plt.savefig(f'./cor_images/p_{i}.png')
		plt.clf()

	# tp = 200
	# cor_p = talib.CORREL(btc_p, dog_p, timeperiod=tp)
	# cor_v = talib.CORREL(btc_v, dog_v, timeperiod=tp)

	# # visualize
	# plt.plot(np.arange(0, len(btc_p)), btc_p)
	# plt.plot(np.arange(0, len(btc_p)), dog_p)
	# plt.plot(np.arange(tp, len(btc_p)), cor_p[tp:])
	# plt.show()
	# plt.clf()

	# plt.plot(np.arange(0, len(btc_v)), btc_v)
	# plt.plot(np.arange(0, len(btc_v)), dog_v)
	# plt.plot(np.arange(tp, len(btc_v)), cor_v[tp:])
	# plt.show()
	# plt.clf()

