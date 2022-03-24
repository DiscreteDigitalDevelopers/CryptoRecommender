'''
Script to scrape metadata from CoinMarketCap
'''
import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()

LIMIT = 150 # limit for calls
TOP = 100 # top N amount of coins to get
API_KEY = os.getenv('CMC_KEY')

if __name__ == '__main__':

	# fetch API
	scraped = []
	black_list = ['USDT', 'USDC']
	data = requests.get(f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY={API_KEY}&limit={LIMIT}').json()
	coin_data = data.get('data')
	i = 0
	for coin in coin_data:
		if coin.get('symbol') in black_list:
			continue
		if i >= TOP:
			break
		c = {}
		c['name'] = coin.get('name')
		c['symbol'] = coin.get('symbol')
		c['market_cap'] = coin.get('quote').get('USD').get('market_cap')
		c['fully_diluted_market_cap'] = coin.get('quote').get('USD').get('market_cap')
		c['circulating_supply'] = coin.get('circulating_supply')
		c['total_supply'] = coin.get('total_supply')
		c['max_supply'] = coin.get('max_supply')
		scraped.append(c)
		print(f'{i}, {c}')
		i += 1

	# save json
	with open('./scraped/metadata.json', 'w') as f:
		json.dump(scraped, f, indent=4)
