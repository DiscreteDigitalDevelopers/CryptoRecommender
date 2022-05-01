from CryptoGraph import CryptoGraph
import sys

def main():
	g = CryptoGraph()
	g.init_from_price_hist(directory = 'Kline/coins')
	g.calculate_regressions()
	g.get_kmeans_clusters()
	g.get_dbscan_clusters()
	g.aggregate_metrics()

	ticker = input('Enter a ticker for similar cryptocurrencies: ')
	while ticker != 'exit':
		# check if ticker is in graph
		if ticker not in g.G:
			print('Ticker is not in graph.\n')
			ticker = input('Enter a ticker for similar cryptocurrencies: ')
			continue

		similar_cryptos = g.get_similar_cryptos(ticker)
		print('Top 10 similar cryptocurrencies:')
		for i, c in enumerate(similar_cryptos):
			if i >= 10:
				break
			print(f'\t{i+1:02d}: {c[0].ljust(10, " ")}   similarity: {c[1]:.6f}')
		print()
		ticker = input('Enter a ticker for similar cryptocurrencies: ')

if __name__ == '__main__':
	main()