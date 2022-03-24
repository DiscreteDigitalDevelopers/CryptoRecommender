import numpy as np
import sys

class Crypto:
	def __init__(self, ticker, price = None, sentiment = None):
		self.ticker = ticker

		if price is None:
			self.price = {}
		else:
			self.price = price

		if sentiment is None:
			self.sentiment = {}
		else:
			self.sentiment = sentiment

	def __repr__(self):
		pass

	def update_price(self, time, price):
		self.price[time] = price

	def plot_price(filename = None):
		x = [i for i in self.price.keys()]
		y = [i for _, i in self.price.items()]
		plt.plot(x, y)
		plt.title(f'Price History of {self.ticker}')
		if filename is None:
			plt.show()
		else:
			plt.savefig(filename)