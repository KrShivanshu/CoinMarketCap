 #This example uses Python 2.7 and the python-request library.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import sys
  
sys.path.insert(0, "D:\Docs\GitHub\CoinMarketCap\head")

from Header import headers


listing_latest_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'100',
  'convert':'USD',
  'sort':'price'
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(listing_latest_url, params=parameters)
  data = json.loads(response.text)
  #print(json.dumps(data, sort_keys=True, indent=4))
  
  for e in data['data']:
    circulating_supply = e['circulating_supply']
    name = e['name']
    market_cap = e['quote']['USD']['market_cap']

    circulating_supply_string = '{:,}'.format(circulating_supply)
    market_cap_string = '{:,}'.format(market_cap)

    print("Name: "+name)
    print("Circulating Supply: "+circulating_supply_string)
    print("Market Cap: "+ market_cap_string)

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)