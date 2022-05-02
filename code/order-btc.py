import requests
import pandas as pd
import time, json
from time import sleep
import FTX
import Report

c = FTX.FTX()

CoinName = input("Coin name you like to watch: ")
MakeTrade = input("Start Trade at percent move(int): ")
Profit = input("Take Profit at this percent(int): ")
Lose = input("Close Trade at this lose percent(int): ")

while True:
    try:
        price_old = requests.get('https://ftx.com/api/markets/' + CoinName).json()
        print(price_old['result']['ask'])
    except Exception as e:
        print(f'Error fetching old coin data:: {e}')

    sleep(10)

    try:
        price_new = requests.get('https://ftx.com/api/markets/' + CoinName).json()
        print(price_new['result']['ask'])
    except Exception as e:
        print(f'Error fetching new coin data: {e}')

    percent = (((float(price_new['result']['ask']) - float(price_old['result']['ask'])) * 100) / float(
        price_old['result']['ask']))

    if percent < float(MakeTrade):
        print(f'No Trade: Percent was under {MakeTrade}%. Percentage move is at {percent}')
        continue

    elif percent >= float(MakeTrade):
        try:
            r = c.place_order("ETH/USD", "buy", 1.0, 0.006)
            print(r)
        except Exception as e:
            print(f'Error making order request: {e}')

        sleep(2)

        try:
            check = c.get_open_orders(r['id'])
        except Exception as e:
            print(f'Error checking for order status: {e}')

        if check[0]['status'] == 'open':
            print('Order placed at {}'.format(pd.Timestamp.now()))
            Report.create_report(CoinName, Lose, Profit)
            break
        else:
            print('Order was either filled or canceled at {}'.format(pd.Timestamp.now()))
            break
