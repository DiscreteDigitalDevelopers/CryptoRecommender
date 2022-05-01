import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import sys
import os
from tqdm import tqdm


# read in data
class DS(torch.utils.data.Dataset):

	def __init__(self, filename, window=200):
		super(DS).__init__()
		# read numpy data
		self.window = window
		self.adj_mat = torch.from_numpy(np.load(filename)).float()
		print(self.adj_mat.shape)

	def __len__(self):
		return self.adj_mat.shape[0] - self.window - 1

	def __getitem__(self, idx):
		return self.adj_mat[idx:idx + self.window], self.adj_mat[idx + self.window]

# model
class model(nn.Module):

	def __init__(self):
		super().__init__()
		# layers
		self.bn1 = nn.BatchNorm2d(num_features=200)
		self.conv1 = nn.Conv2d(200, 128, kernel_size=1)
		self.bn2 = nn.BatchNorm2d(num_features=128)
		self.conv2 = nn.Conv2d(128, 64, kernel_size=3, dilation=3, padding=3)
		self.bn3 = nn.BatchNorm2d(num_features=64)
		self.conv3 = nn.Conv2d(64, 8, kernel_size=1)

	def forward(self, x):
		# project down channels
		x = F.elu(self.bn1(x))
		x = self.conv1(x)
		
		# dilation
		x = F.elu(self.bn2(x))
		x = self.conv2(x)
		
		# project back
		x = F.elu(self.bn3(x))
		x = self.conv3(x)
		
		return x

if __name__ == '__main__':
	ds = DS('adj_mat.npy')
	data, label = ds.__getitem__(300)
	data = data.unsqueeze(0).float()
	
	# train loop 	
	# print(f'original size: {data.shape}')
	# net = model()
	# pred = net(data)
	# pred = torch.tanh(torch.mean(pred,dim=1))

	# print(f'after conv size: {pred.shape}')

	# dataloader
	dataloader = torch.utils.data.DataLoader(ds, batch_size=10, shuffle=True)
	net = model().cuda()
	optimizer = torch.optim.Adam(net.parameters(), lr=0.01)
	# for i in range(50):
	# 	sum_loss = 0
	# 	for data, label in tqdm(dataloader):
	# 		data, label = data.cuda(), label.cuda()

	# 		optimizer.zero_grad()

	# 		pred = net(data)
	# 		pred = torch.tanh(torch.mean(pred,dim=1))

	# 		# loss
	# 		loss = F.mse_loss(pred, label)
	# 		sum_loss += loss.item()

	# 		loss.backward()
	# 		optimizer.step()

	# 	# output stats
	# 	sum_loss /= len(dataloader.dataset)
	# 	print(f'loss={sum_loss}')
	# # save model weights
	# torch.save(net.state_dict(), f'./best_w.pt')

	net.load_state_dict(torch.load('./best_w.pt'))
	net.eval()
	frames = 800
	# generate next 800 frames
	timeseries = ds.adj_mat.clone().cuda()
	for idx, f in tqdm(enumerate(range(frames))):
		# print(f'{timeseries.shape=}')
		data = timeseries[-200:].unsqueeze(0)
		# print(data.shape)
		pred = net(data)
		pred = torch.tanh(torch.mean(pred,dim=1)).view(1,18,18)
		timeseries = torch.cat((timeseries, pred), dim=0)
		# print(timeseries.shape)
	print(timeseries.shape)
	print(timeseries[-1])
	np.save('cor_pred_800.npy', timeseries.cpu().detach().numpy())


	# print(data.shape)
	# print(data[-1])
	# print(label.shape)
	# print(label)