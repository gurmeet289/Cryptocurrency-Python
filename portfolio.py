import os
import csv
import json
import requests
from prettytable import PrettyTable
import colorama
from colorama import Fore, Back, Style
# You can say in windows or in python3 you have to import colorama and colorama.init()
colorama.init()



local_currency = 'USD'
local_symbol = '$'

api_key = 'f44c1b47-d50e-482d-86b3-2d4db48ce124'#'1c88dcb6-eec2-4a68-8ee5-305ec6466c58'
headers = {'X-CMC_PRO_API_KEY': api_key}

base_url = 'https://pro-api.coinmarketcap.com'

print()
print("MY PORTFOLIO")
print()

portfolio_value = 0.00
last_updated = 0

table = PrettyTable(['Asset', 'Amount Owned', 'Price','Value', '1h', '24h', '7d'])

with open("my_portfolio.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        #For mac
        # if '\ufeff' in line[0]:
        #     symbol = line[0][1:].upper()
        #     print(symbol)
        # else:
        #     symbol = line[0].upper()
            #print(symbol)
        symbol = line[0].upper()
        #print(symbol)
        amount = line[1]

        ticker_url = base_url + '/v1/cryptocurrency/quotes/latest?convert=' + local_currency + '&symbol=' + symbol

        request = requests.get(ticker_url, headers=headers)
        results = request.json()

        #print(json.dumps(results, sort_keys=True, indent=4))

        currency = results['data'][symbol]

        name = currency['name']
        quotes = currency['quote'][local_currency]
        hour_change = round(quotes['percent_change_1h'],1)
        #print('hour', hour_change)
        day_change = round(quotes['percent_change_24h'],1)
        #print('day change', day_change)
        week_change = round(quotes['percent_change_7d'],1)
        #print('week change', week_change)
        price = quotes['price']

        value = float(price) * float(amount)


        if hour_change > 0:
            hour_change = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
        else:
            hour_change = Back.RED + str(hour_change) + '%' + Style.RESET_ALL

        if day_change > 0:
            day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
        else:
            day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL

        if week_change > 0:
            week_change = Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
        else:
            week_change = Back.RED + str(week_change) + '%' + Style.RESET_ALL

        portfolio_value += value


        price_string = '{:,}'.format(round(price,2))
        value_string = '{:,}'.format(round(value,2))

        table.add_row([name + ' (' + symbol + ')',
                   amount,
                   local_symbol + price_string,
                   local_symbol + value_string,
                   str(hour_change),
                   str(day_change),
                   str(week_change)])

print(table)
print()

portfolio_value_string = '{:,}'.format(round(portfolio_value,2))
print('Total Portfolio Value: ' + Back.GREEN + local_symbol + portfolio_value_string + Style.RESET_ALL)
print()
