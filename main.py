from CryptoGraph import CryptoGraph
import sys

def main():
	g = CryptoGraph()
	g.init_from_price_hist(directory = 'Kline/filter')
	g.calculate_regressions(plot_best = True)
	g.import_correlation_data()
	print(g)
	# print(g.get_edge('ADAUSDT', 'AVAXUSDT')[1].pair_data)
	g.edges_to_file('cg.edges')

if __name__ == '__main__':
	main()