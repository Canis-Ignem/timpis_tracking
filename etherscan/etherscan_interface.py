import requests
import json

login_data = ""
with open('login', 'r') as f:
    login_data = json.load(f)

def get_eth_price():

    price = requests.get('https://api.etherscan.io/api?module=stats&action=ethprice&apikey=EJJ58HMPEPIUJQ4QPTHYRP3XSJYQE946H1}')
    data = json.loads(price.text)

    return float(data.get('result')['ethusd']), float(data.get('result')['ethbtc'])


print(get_eth_price())