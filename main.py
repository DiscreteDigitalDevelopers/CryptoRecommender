from CryptoGraph import CryptoGraph

def main():
	g = CryptoGraph()
	g.init_from_price_hist(directory = 'Kline/filter')
	g.calculate_regressions()
	g.import_correlation_data()
	print(g)
	print(g.get_edge('ADAUSDT', 'AVAXUSDT')[1].pair_data)

if __name__ == '__main__':
	main()