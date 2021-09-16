from kucoin.client import Client
import pandas as pd
import time
import json
login_data = ""
with open('login', 'r') as f:
    login_data = json.load(f)

client = Client(login_data["kucoin"]["key"], login_data["kucoin"]["secret"], login_data["kucoin"]["passphrase"])

LTX  = {'name':'LTX', 'ticker':"LTX-USDT"}
TEL  = {'name':'TEL', 'ticker':"TEL-USDT"}
ATOM = {'name':'ATOM', 'ticker':"ATOM-USDT"}

def get_balance():

    df = pd.DataFrame(client.get_accounts()).drop(['id','type'] , axis=1).set_index('currency').astype(float)
    df = df[ df['balance'] !=0  ]
    return df

def get_total():
    total = 0
    df = pd.DataFrame(client.get_accounts()).drop(['id','type'] , axis=1).set_index('currency').astype(float)
    df = df[ df['balance'] !=0  ]

    for i in range(len(df)):
        
        if df.index[i] == 'USDT':
            total += df.balance[i]
        else:
            total += df['balance'][i] * float(client.get_ticker(df.index[i] + '-USDT')['price'])
    return total

def get_coin_balance(coin):
    df = pd.DataFrame(client.get_accounts()).drop(['id','type'] , axis=1).set_index('currency').astype(float)

    return df.loc[coin['name']]['balance']

def coin_to_dollar(coin):

    balance = get_coin_balance(coin)
    price = float(client.get_ticker(coin['ticker'])['price'])

    return balance * price

def check_price(coin_name):
    return float(client.get_ticker(coin_name + '-USDT')['price'])

def buy(coin, spend, price):
    
    order = client.create_limit_order(coin['ticker'], Client.SIDE_BUY, str(spend/price),str(price))
    return order

def sell(coin, pct, price):

    balance = get_coin_balance(coin)

    order = client.create_limit_order(coin['ticker'], Client.SIDE_SELL, str(pct*balance) ,str(price))
    return order
