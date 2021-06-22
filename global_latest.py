from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import sys
  
sys.path.insert(0, "D:\Docs\GitHub\CoinMarketCap\head")

from Header import headers

currency = 'INR'

global_latest_url = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest?convert='+currency

session = Session()
session.headers.update(headers)


try:
    response = session.get(global_latest_url)
    data = json.loads(response.text)
    #print(json.dumps(data, sort_keys=True, indent=4))

    active_currencies = data['data']['active_cryptocurrencies']
    active_exchanges = data['data']['active_exchanges']

    active_currencies_string = '{:,}'.format(active_currencies)
    active_exchanges_string = '{:,}'.format(active_exchanges)

    print('There are currently '+ active_currencies_string + ' active cryptocurrencies.')
    print('Active market is '+active_exchanges_string + '.')

except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)