import numpy as np
import sys
from datetime import datetime as dt

class Crypto:
	def __init__(self, ticker, price = None, data = None):
		self.ticker = ticker
		self.last_price = None

		if price is None:
			self.price = {}
		else:
			self.price = price

		if data is None:
			self.data = {}
		else:
			self.data = data

	def __repr__(self):
		return f'{self.ticker}: ${float(self.last_price[1]):.2f} at {self.from_unix(self.last_price[0])}'

	def update_price(self, timestamp, p):
		self.price[timestamp] = p
		self.last_price = (timestamp, p)

	def update_data(self, timestamp, d):
		self.data[timestamp] = d

	def get_timestamp_list(self):
		return np.array([i for i in self.price.keys()])

	def get_price_list(self):
		return np.array([i for _, i in self.price.items()])

	def plot_price(self, filename = None):
		x = self.get_timestamp_list()
		y = self.get_price_list()
		plt.plot(x, y)
		plt.title(f'Price History of {self.ticker}')
		if filename is None:
			plt.show()
		else:
			plt.savefig(filename)

	def normalized_price(self):
		y = self.get_price_list()
		y /= np.max(y)
		return y

	@staticmethod
	def to_unix(d):
		return int(d.timestamp())

	@staticmethod
	def from_unix(unix_time):
		return dt.fromtimestamp(unix_time)