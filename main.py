from CryptoGraph import CryptoGraph

def main():
	g = CryptoGraph()
	g.init_from_file('tickers.txt')
	g.update_prices()
	print(g)

if __name__ == '__main__':
	main()