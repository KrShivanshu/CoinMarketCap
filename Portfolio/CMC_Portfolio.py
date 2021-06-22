import os
import json
from requests import Request, Session
from datetime import datetime
from prettytable import PrettyTable
from colorama import Fore, Back, Style
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import sys
  
sys.path.insert(0, "D:\Docs\GitHub\CoinMarketCap\head")

from Header import headers

listing_latest_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'convert':'INR'
}

session =Session()
session.headers.update(headers)

try:
    response = session.get(listing_latest_url, params=parameters)
    results = json.loads(response.text)
    data = results['data']
    tracking_url_pair = {}
    for currency in data:
        symbol = currency['symbol']
        url = currency['id']
        tracking_url_pair[symbol]=url
        ##print(str(symbol)+":"+str(tracking_url_pair[symbol]))

    print()
    print("My Portfolio")
    print()

    portfolio_value = 0.00
    last_updated = 0

    table = PrettyTable(['Assets',"Assets Owned", parameters['convert'] + 'Value', 'Price','1h','24h','7d'])

    with open("Portfolio\portfolio.txt") as inp:
        for line in inp:
            ticker, amount = line.split()
            tikcer = ticker.upper()

            ticker_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
            specific_parameters = {
                'symbol':ticker,
                'convert':'INR',
            }
            specific_response = session.get(ticker_url, params=specific_parameters)
            specific_results = json.loads(specific_response.text)
            # print(json.dumps(specific_results, sort_keys=True, indent=4))
            currency = specific_results['data'][ticker.upper()]
            rank = currency['cmc_rank']
            name = currency['name']
            last_updated = currency['last_updated']
            symbol = currency['symbol']
            quotes = currency['quote'][specific_parameters['convert']]
            hour_change = quotes['percent_change_1h']
            day_change = quotes['percent_change_24h']
            week_change = quotes['percent_change_7d']
            price = quotes['price']

            value = float(price)*float(amount)

            if int(hour_change)>0:
              hour_change=Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
            else:
              hour_change=Back.RED + str(hour_change) + '%' + Style.RESET_ALL

            if day_change>0:
              day_change=Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
            else:
              day_change=Back.RED + str(day_change) + '%' + Style.RESET_ALL
            
            if week_change>0:
              week_change=Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
            else:
              week_change=Back.RED + str(week_change) + '%' + Style.RESET_ALL
            

            portfolio_value += value

            value_string = '{:,}'.format(round(value,2))
            
            table.add_row([name+' ('+symbol+')',
            amount,
            '$'+value_string,
            '$'+str(price),
            str(hour_change),
            str(day_change),
            str(week_change)])
    
    print(table)
    print()

    portfolio_value_string = '{:,}'.format(round(portfolio_value,2))
    last_updated_string = datetime.fromisoformat(last_updated[:-1]).strftime('%Y-%m-%d %H:%M:%S')

    print("Total Portfolio Value: "+ Back.BLUE + portfolio_value_string + Style.RESET_ALL)
    print()
    print("API results last updated on "+ last_updated_string)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)