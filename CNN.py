import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data as du
from torch.utils.data import IterableDataset

import numpy as np
import sys
import csv
from os import listdir
from tqdm import tqdm

# CONSTANTS
batch_size = 100
learning_rate = 0.001
num_epochs = 10
progress_bar = True

class Price_Dataset(IterableDataset):
	def __init__(self, directory, window_size = 100, start = 0, end = 8):
		super().__init__()

		self.window_size = window_size

		prices = []
		files = listdir(directory)
		csvs = [f'{directory}/{f}' for f in files if f.endswith('csv')][start:end]
		for c in csvs:
			with open(c, 'r') as f:
				lines = list(csv.reader(f))[1:]
				prices.append(np.array([float(l[5]) for l in lines]))
		prices = np.array(prices)
		for i, row in enumerate(prices):
			for j, col in enumerate(row[:-1]):
				prices[i][j] -= prices[i][j+1]

		self.prices = prices
		self.length = int(len(self.prices)*(
			(len(self.prices[0]) - self.window_size-1)+(len(self.prices[0]) - self.window_size-1)//2+
			(len(self.prices[0]) - self.window_size-1)//3+(len(self.prices[0]) - self.window_size-1)//4+
			(len(self.prices[0]) - self.window_size-1)//5))

	def __len__(self):
		return self.length

	def __iter__(self):
		for p in self.prices:
			for k in np.arange(1, 5):
				for offset in range(0, (len(p) - self.window_size-1)//k):
					out = torch.zeros(self.window_size)
					for i in range(self.window_size):
						out[i] = np.sum(p[offset+i*k:offset+(i+1)*k])
					out = out.unsqueeze(1)
					# label = 1 if np.sum(p[offset+self.window_size*k:offset+(self.window_size+1)*k]) > 0 else 0
					label = np.sum(p[offset+self.window_size*k:offset+(self.window_size+1)*k])
					yield out, label


class CNN_Model(nn.Module):
	def __init__(self, in_dim, hidden_dim):
		super().__init__()

		self.lstm = nn.LSTM(in_dim, hidden_dim, num_layers = 1, batch_first = True)
		self.fc1 = nn.Linear(hidden_dim, hidden_dim//2)
		self.fc2 = nn.Linear(hidden_dim//2, 1)

	def forward(self, x):
		out, (hn, cn) = self.lstm(x)
		x = hn[0, :, :]
		x = torch.tanh(x)
		x = self.fc1(x)
		x = torch.tanh(x)
		x = self.fc2(x)
		x = torch.tanh(x)
		return x

def main():
	device = f'cuda:0' if torch.cuda.is_available() else 'cpu'
	print(f"using device: {device}")

	train_dataset = Price_Dataset('Kline/filter', window_size = 10, start = 0, end = 4)
	train_loader = du.DataLoader(dataset = train_dataset, batch_size = batch_size)

	test_dataset = Price_Dataset('Kline/filter', window_size = 10, start = 4, end = 7)
	test_loader = du.DataLoader(dataset = test_dataset, batch_size = batch_size)

	model = CNN_Model(1, 10)
	model = model.to(device)
	model.train()

	optimizer = optim.Adam(model.parameters(), lr = learning_rate)

	loss_func = nn.MSELoss()

	for epoch in range(num_epochs):
		sum_loss = 0
		for batch_idx, (price, label) in enumerate(tqdm(train_loader, disable = not progress_bar)):
			price, label = price.to(device), label.unsqueeze(1).to(device)

			optimizer.zero_grad()

			pred = model(price)

			loss = loss_func(pred.float(), label.float())
			loss.backward()

			optimizer.step()

			sum_loss += loss.item()

		print(f'Epoch {epoch}: Train loss: {sum_loss/batch_idx/batch_size:.8f}')

	model.eval()
	with torch.no_grad():
		correct = 0
		incorrect = 0
		for batch_idx, (price, label) in enumerate(tqdm(test_loader, disable = not progress_bar)):
			price, label = price.to(device), label.unsqueeze(1).to(device)

			pred = model(price)

			loss = loss_func(pred.float(), label.float())

			sum_loss += loss.item()

	print(f'Test accuracy: {sum_loss/batch_idx/batch_size:.4f}')

if __name__ == '__main__':
	main()