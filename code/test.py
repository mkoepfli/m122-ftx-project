import json

import json2html
import json2table as json2table
import requests

#All Markets
response = requests.get("https://ftx.com/api/markets").json()
print(response)

#All Futures
response = requests.get("https://ftx.com/api/futures").json()
print(response)

#Specific Future
response = requests.get("https://ftx.com/api/futures/ABNB-0624").json()
print(response)