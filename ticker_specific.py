#This example uses Python 2.7 and the python-request library.

#this program and api extract data for specific coin (CMC id map)
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import sys
  
sys.path.insert(0, "D:\Docs\GitHub\CoinMarketCap\head")

from Header import headers


listing_latest_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
    'id':'1',
    'convert':'USD'
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(listing_latest_url, params=parameters)
    data = json.loads(response.text)
    print(json.dumps(data, sort_keys=True, indent=4))
    f = data['data']
    for key in f:
        circulating_supply = f[key]['circulating_supply']
        name = f[key]['name']
        market_cap = f[key]['quote'][parameters['convert']]['market_cap']

        circulating_supply_string = '{:,}'.format(circulating_supply)
        market_cap_string = '{:,}'.format(market_cap)

        print("Name: \t\t\t"+name)
        print("Circulating Supply: \t"+circulating_supply_string)
        print("Market Cap: \t\t"+ market_cap_string)
        print()

except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)