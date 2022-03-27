from CryptoGraph import CryptoGraph

def main():
	g = CryptoGraph()
	g.init_from_price_hist()
	g.calculate_correlations()

if __name__ == '__main__':
	main()