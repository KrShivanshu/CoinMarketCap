import os
import json
import time
from say import *
from datetime import datetime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import win32com.client as wincl

import sys

sys.path.insert(0, "D:\Docs\GitHub\CoinMarketCap\head")

from Header import headers


speak = wincl.Dispatch("SAPI.SpVoice")
""""
listing_latest_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters ={
    'convert':'INR'
}
""" 

session =Session()
session.headers.update(headers)
  
try:
    """
    response = session.get(listing_latest_url, params = parameters)
    results = json.loads(response.text)
    data = results['data']
    tracking_url_pair = {}
    for currency in data:
        symbol = currency['symbol']
        url = currency['id']
        tracking_url_pair[symbol]=url
    """

    print()
    print("Alert System")
    print()

    already_hit_symbols=[]

    while True:
        with open("AlertSystem\Target.txt") as inp:
            for line in inp:
                ticker, target = line.split()
                ticker = ticker.upper()
                print(ticker)

                ticker_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
                specific_parameters = {
                'symbol':ticker.upper(),
                'convert':'INR',
                }
                specific_response = session.get(ticker_url, params=specific_parameters)
                specific_results = json.loads(specific_response.text)

                currency = specific_results['data'][ticker.upper()]
                name = currency['name']
                last_updated = currency['last_updated']
                symbol = currency['symbol']
                quotes = currency['quote'][specific_parameters['convert']]
                price = quotes['price']

                if float(price)>=float(target) and symbol not in already_hit_symbols:
                    speak.Speak(name + 'hit the target of ' + target + ' Rupees')
                    
                    last_updated_string = datetime.fromisoformat(last_updated[:-1]).strftime('%Y-%m-%d %H:%M:%S')
                    print(name+' hit '+target+' on '+last_updated_string)
                    already_hit_symbols.append(symbol)
                else:
                    print(name+' did not hit the '+ str(target) +' current price is only '+str(price))

        print("...")
        time.sleep(10)
    
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)