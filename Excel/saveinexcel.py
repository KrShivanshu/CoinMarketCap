import xlsxwriter
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import sys
  
sys.path.insert(0, "D:\Docs\GitHub\CoinMarketCap\head")

from Header import headers

start = 1
f = 1
s='(₹)'
crypto_workbook = xlsxwriter.Workbook('cryptocurrencies.xlsx')
crypto_sheet = crypto_workbook.add_worksheet()

bold = crypto_workbook.add_format({'bold':1})


crypto_sheet.write('A1','Name',bold)
crypto_sheet.write('B1','Symbol',bold)
crypto_sheet.write('C1','Market Cap '+s,bold)
crypto_sheet.write('D1','Price '+s,bold)
crypto_sheet.write('E1','24H volume '+s,bold)
crypto_sheet.write('F1','Hour Change (%)',bold)
crypto_sheet.write('G1','Day Change (%)',bold)
crypto_sheet.write('H1','Week Change (%)',bold)

# it sets the column witdth
crypto_sheet.set_column('A:A',15)
crypto_sheet.set_column('B:B',15)
crypto_sheet.set_column('C:C',15)
crypto_sheet.set_column('D:D',15)
crypto_sheet.set_column('E:E',15)
crypto_sheet.set_column('F:F',15)
crypto_sheet.set_column('G:G',15)
crypto_sheet.set_column('H:H',15)

listing_latest_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

session = Session()
session.headers.update(headers)

for i in range(1):
    parameters = {
    'start':start,
    'limit':start+100,
    'convert':'INR'
    }

    try:
        response = session.get(listing_latest_url, params=parameters)
        data = json.loads(response.text)
        #print(json.dumps(data, sort_keys=True, indent=4))
        
        for currency in data['data']:
            rank = currency['cmc_rank']
            name = currency['name']
            symbol = currency['symbol']
            quotes = currency['quote'][parameters['convert']]
            hour_change = quotes['percent_change_1h']
            hour_change = '{:,}'.format(round(hour_change,2))
            day_change = quotes['percent_change_24h']
            day_change = '{:,}'.format(round(day_change,2))
            week_change = quotes['percent_change_7d']
            week_change = '{:,}'.format(round(week_change,2))
            price = quotes['price']
            price = '{:,}'.format(round(price,6))
            volume = quotes['volume_24h']
            volume = '{:,}'.format(round(volume,2))
            market_cap = quotes['market_cap']
            market_cap = '{:,}'.format(round(market_cap,2))

            crypto_sheet.write(f,0,name)
            crypto_sheet.write(f,1,symbol)
            crypto_sheet.write(f,2,str(market_cap))
            crypto_sheet.write(f,3,str(price))
            crypto_sheet.write(f,4,str(volume))
            crypto_sheet.write(f,5,str(hour_change))
            crypto_sheet.write(f,6,str(day_change))
            crypto_sheet.write(f,7,str(week_change))

            f+=1

        start+=100
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

print("Done! Look for excel file in disk")
crypto_workbook.close()


