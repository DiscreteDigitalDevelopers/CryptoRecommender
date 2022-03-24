import numpy as np
import sys
import random
import matplotlib.pyplot as plt

sys.setrecursionlimit(10000)

class Graph:
	def __init__(self):
		self.adj_list = {}

	def __len__(self):
		return len(self.adj_list)

	def __repr__(self):
		out = ''
		for i, row in self.adj_list.items():
			row = sorted(row)
			if(len(row) == 0):
				out += str(i)+': {}\n'
			else:
				out += str(i)+': {'
				for j in row:
					out += str(j)+', '
				out += '}\n'
		out = out.replace(', }','}')
		return out

	def num_edges(self):
		edges = 0
		for i, row in self.adj_list.items():
			edges += len(row)
		return edges//2

	def average_degree(self):
		return 2*self.num_edges()/len(self)

	def add_node(self, u):
		if u not in self.adj_list:
			self.adj_list[u] = set()

	def add_edge(self, u, v):
		self.adj_list[u].add(v)

	def has_edge(self, u, v):
		if v in self.adj_list[u]:
			return True
		else:
			return False

	def remove_edge(self, u, v):
		self.adj_list[u].discard(v)

	def get_edges(self):
		edges = set()
		for i, row in self.adj_list.items():
			for j in row:
				if (j,i) not in edges:
					edges.add((i,j))
		return list(edges)

	def remove_node(self, node):
		if node not in self.adj_list.keys():
			return
		for i in self.adj_list[node]:
			self.adj_list[i].discard(node)
		del self.adj_list[node]

	def remove_nodes(self, nodes):
		for node in nodes:
			self.remove_node(node)

	def DFS(self, u):
		self.visited[u] = True
		self.comp.append(u)
		for i in self.adj_list[u]:
			if not self.visited[i]:
				self.DFS(i)

	def find_connected_components(self):
		self.cc = []
		self.visited  = [False for i in range(max(self.adj_list.keys())+1)]
		for i in self.adj_list.keys():
			if not self.visited[i]:
				self.comp = []
				self.DFS(i)
				self.cc.append(sorted(self.comp))
		self.cc.sort()
		return self.cc

	def largest_connected_component(self):
		l_cc = []
		for comp in self.cc:
			if len(comp) > len(l_cc):
				l_cc = comp
		return l_cc
	def plot_degree_dist(self, filename):
		degrees = []
		for i, row in self.adj_list.items():
			degrees.append(len(row))
		x = [i for i in range(max(degrees)+1)]
		y = [0 for i in range(max(degrees)+1)]
		for i in degrees:
			y[i] += 1
		plt.scatter(x,y)
		plt.yscale('log')
		plt.xscale('log')
		plt.xlim([0.5,2*max(x)])
		plt.ylim([0.5,2*max(y)])
		plt.title('Degree Distribution')
		plt.xlabel("k")
		plt.ylabel("P(k)")
		plt.savefig(filename)
		plt.clf()

	def plot_cumulative_degree_dist(self, filename):
		degrees = []
		for i, row in self.adj_list.items():
			degrees.append(len(row))
		x = [i for i in range(max(degrees)+1)]
		y = [0 for i in range(max(degrees)+1)]
		for i in degrees:
			y[i] += 1
		for i in range(len(y)):
			y[i] = sum(y[i:])
		plt.scatter(x,y)
		plt.yscale('log')
		plt.xscale('log')
		plt.xlim([0.5,2*max(x)])
		plt.ylim([0.5,2*max(y)])
		plt.title('Cumulative Degree Distribution')
		plt.xlabel("k")
		plt.ylabel("P(k)")
		plt.savefig(filename)
		plt.clf()

	def edges_to_file(self, filename):
		f = open(filename, 'w')
		s = 'Source Target\n'
		for i, row in self.adj_list.items():
			for j in row:
				s += f'{i} {j}\n'
		f.write(s)
		f.close()

	def adj_list_to_file(self, filename):
		f = open(filename, 'w')
		f.write(self.to_string())
		f.close()

	def read_adj_list_from_file(self, filename):
		with open(filename) as f:
			lines = f.readlines()
			for row in lines:
				self.add_node(int(row.split(':')[0]))
			for row in lines:
				u = int(row.split(':')[0])
				vals = row.split(': ')[1][1:-2].split(', ')
				for i in range(len(vals)):
					self.add_edge(u,int(vals[i]))

	def remove_percent_nodes(self, p):
		G_removed = self
		nodes = random.sample(list(G_removed.adj_list.keys()),int(p*len(G_removed)))
		G_removed.remove_nodes(nodes)
		return G_removed