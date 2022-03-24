import numpy as np
import sys

class Crypto:
	def __init__(self, ticker, price_hist = None):
		self.ticker = ticker
		if price_hist is None:
			self.price_hist = {}
		else:
			self.price_hist = price_hist

	def __repr__(self):
		pass

	def update_price(self, time, price):
		self.price_hist[time] = price

	def plot_price_hist(filename = None):
		x = [i for i in self.price_hist.keys()]
		y = [i for _, i in self.price_hist.items()]
		plt.plot(x, y)
		plt.title(f'Price History of {self.ticker}')
		if filename is None:
			plt.show()
		else:
			plt.savefig(filename)