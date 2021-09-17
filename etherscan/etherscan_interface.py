import requests
import json
from kucoin.client import Client
login_data = ""
with open('login', 'r') as f:
    login_data = json.load(f)

def get_eth_price():

    price = requests.get('https://api.etherscan.io/api?module=stats&action=ethprice&apikey={}'.format(login_data['etherscan']['key']))
    data = json.loads(price.text)

    return float(data.get('result')['ethusd']), float(data.get('result')['ethbtc'])

def get_account_balance(address):

    balance = requests.get('https://api.etherscan.io/api?module=account&action=balance&address={}&tag=latest&apikey={}'.format(address, login_data['etherscan']['key']))
    data = json.loads(balance.text)

    return float(data.get('result'))/1000000000000000000

def get_account_balance_usd(address):
    eth = get_account_balance(address)
    usd, _ = get_eth_price()
    return eth * usd

def get_token_balance(token, address):

    balance = requests.get('https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={}&address={}&tag=latest&apikey={}'.format(token, address, login_data['etherscan']['key']))
    data = json.loads(balance.text)

    return float(data.get('result'))/10**18


def get_token_price_usd(token_name):

    client = Client(login_data["kucoin"]["key"], login_data["kucoin"]["secret"], login_data["kucoin"]["passphrase"])

    return float(client.get_ticker(token_name.upper() + '-USDT')['price'])

def get_token_price_eth(token_name):

    client = Client(login_data["kucoin"]["key"], login_data["kucoin"]["secret"], login_data["kucoin"]["passphrase"])

    return float(client.get_ticker(token_name.upper() + '-ETH')['price'])

def get_token_balance_usd(token, token_name, address):

    balance = get_token_balance(token, address)
    price = get_token_price_usd(token_name)

    return balance * price

def get_token_balance_eth(token, token_name, address):

    balance = get_token_balance(token, address)
    price = get_token_price_eth(token_name)

    return balance * price

res = get_token_balance_eth(login_data['etherscan']['boson'] ,"boson", login_data['etherscan']['address'])
print(res)
