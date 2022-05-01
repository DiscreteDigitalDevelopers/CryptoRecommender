import numpy as np
import csv
import os
from matplotlib import pyplot as plt
import talib
import networkx as nx
from tqdm import tqdm
import sys


if __name__ == '__main__':
	
	L = 18
	tp = 200

	# read prediction results
	adj_mat = np.load('cor_pred_800.npy')

	# create Graph
	G = nx.complete_graph(L)
	for e in G.edges.data():
		e[2]['price'] = adj_mat[:, e[0], e[1]]
		e[2]['volume'] = adj_mat[:, e[1], e[0]]

	# visualize 
	pos = nx.spring_layout(G, seed=69)
	for i in tqdm(range(1800 - tp)):
		edges, weights = zip(*nx.get_edge_attributes(G,'price').items())
		weights = [w[i] for w in weights]
		nx.draw(G, pos=pos, edgelist=edges, edge_color=weights, edge_cmap=plt.cm.cool, with_labels=True)
		plt.savefig(f'./cor_images/p_{i}.png')
		plt.clf()