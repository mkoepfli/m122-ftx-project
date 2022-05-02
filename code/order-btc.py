import requests
import pandas as pd
import time, json
from time import sleep
import FTX
import Report

c = FTX.FTX()

# Get User Inputs
coin_name = input("Coin name you like to watch: ")
make_trade = input("Start Trade at percent move(int): ")
profit = input("Take Profit at this percent(int): ")
lose = input("Close Trade at this lose percent(int): ")
time_wait = input("Waiting time for next price(seconds): ")

while True:
    try:
        # Get Coin price and save it to price_old variable
        price_old = requests.get('https://ftx.com/api/markets/' + coin_name).json()
        # Print Price in the console
        print(price_old['result']['ask'])
    except Exception as e:
        # Write Error in console if an error shows up
        print(f'Error fetching old coin data:: {e}')

    sleep(float(time_wait))

    try:
        # Get Price after time wait and save it to price_new variable
        price_new = requests.get('https://ftx.com/api/markets/' + coin_name).json()
        # Print Price in the console
        print(price_new['result']['ask'])
    except Exception as e:
        # Write Error in console if an error shows up
        print(f'Error fetching new coin data: {e}')

    # Calculate the percent between those 2 Prices
    percent = (((float(price_new['result']['ask']) - float(price_old['result']['ask'])) * 100) / float(
        price_old['result']['ask']))

    # Check if percent is under the make_trade value
    if percent < float(make_trade):
        # If true -> Write in console and continue with next price after waiting time
        print(f'No Trade: Percent was under {make_trade}%. Percentage move is at {percent}')
        continue

    # If percent is over make_trade
    elif percent >= float(make_trade):
        try:
            # If true, place an Order
            r = c.place_order("ETH/USD", "buy", 1.0, 0.006)
            print(r)
        except Exception as e:
            # Write Error in console if an error shows up
            print(f'Error making order request: {e}')

        sleep(2)

        try:
            check = c.get_open_orders(r['id'])
        except Exception as e:
            # Write Error in console if an error shows up
            print(f'Error checking for order status: {e}')

        if check[0]['status'] == 'open':
            # Write in console that order was placed at current timestamp
            print('Order placed at {}'.format(pd.Timestamp.now()))
            # Create Report
            Report.create_report(coin_name, price_new['result']['ask'], lose, profit)
            break
        else:
            print('Order was either filled or canceled at {}'.format(pd.Timestamp.now()))
            break
