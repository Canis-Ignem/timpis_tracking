import pandas as pd
from binance.client import Client
from binance.enums import *
from time import time, sleep
import json

login_data = ""
with open('login', 'r') as f:
    login_data = json.load(f)

client = Client(login_data['binance']['key'],
                login_data['binance']['secret'])

# TICKERS
BTC  = {'name':'BTC', 'ticker':"BTCUSDT"}
ETH  = {'name':'ETH', 'ticker':"ETHUSDT"}
ADA  = {'name':'ADA', 'ticker':"ADAUSDT"}
VET  = {'name':'VET', 'ticker':"VETUSDT"}
BNB  = {'name':'BNB', 'ticker':"BNBUSDT"}
LINK = {'name':'LINK', 'ticker':"LINKUSDT"}


SPOT = pd.DataFrame(client.get_account_snapshot(type='SPOT')['snapshotVos'][0]['data']['balances']).set_index('asset')
SPOT = SPOT.loc[((SPOT['free'] != '0') | (SPOT['locked'] != '0'))]
SPOT = SPOT[SPOT.columns].astype(float)

TOTAL_BTC = float(client.get_account_snapshot(type='SPOT')['snapshotVos'][0]['data']['totalAssetOfBtc'])

def get_USDT(coin):
    total = SPOT.loc[coin['name']].sum()
    ticker = float(client.get_symbol_ticker(symbol=coin['ticker'])['price'])
    return  total * ticker

def get_total_USDT():
    ticker = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
    return  TOTAL_BTC  * ticker

def buy(coin, spend, price, test = 1):

  if test == 1:
    try:
      buy_limit = client.create_test_order(
          symbol = coin['ticker'],
          side = SIDE_SELL,
          type = ORDER_TYPE_LIMIT,
          timeInForce = TIME_IN_FORCE_GTC,
          quantity = "%.5f" % (spend/price),
          price = price
        )
      print(buy_limit)
    except:
      buy_limit ="ERROR"
      print("Something went wrong")
  else:
    try:
      buy_limit = client.create_order(
        symbol = coin['ticker'],
        side = SIDE_SELL,
          type = ORDER_TYPE_LIMIT,
          timeInForce = TIME_IN_FORCE_GTC,
        quantity = "%.5f" % (spend/price),
        price = price
        )
      print(buy_limit)
    except:
      buy_limit ="ERROR"
      print("Something went wrong")
  return buy_limit

def sell(coin, pct, price, test = 1):
  
  if test == 1:
    try:
        
        sell_limit = client.create_test_order(
          symbol = coin['ticker'],
          side = SIDE_SELL,
          type = ORDER_TYPE_LIMIT,
          timeInForce = TIME_IN_FORCE_GTC,
          quantity = round(SPOT.loc[coin['name']]['free']  * pct, 5),
          price = str(price)
        )

        print(SPOT.loc[coin['name']]['free']  * pct)
        print(sell_limit)

    except:
      sell_limit ="ERROR"
      print("Something went wrong")

  else:
    try:
        sell_limit = client.create_order(
            symbol = coin['ticker'],
            side = SIDE_SELL,
            type = ORDER_TYPE_LIMIT,
            timeInForce = TIME_IN_FORCE_GTC,
            quantity = round(SPOT.loc[coin['name']]['free']  * pct, 5),
            price = str(price)
            )
        print(sell_limit)
    except:
      sell_limit ="ERROR"
      print("Something went wrong")
  return sell_limit


balance = client.get_asset_balance(asset='BNB')
print(balance)