from CryptoGraph import CryptoGraph

def main():
	g = CryptoGraph()
	g.init_from_price_hist(directory = 'Kline/filter')
	g.calculate_regressions()
	print(g)

if __name__ == '__main__':
	main()