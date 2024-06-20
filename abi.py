# from web3 import Web3

# # Подключение к нодам
# w3_el = Web3(Web3.HTTPProvider('http://34.88.58.174:8545/'))
# w3_cl = Web3(Web3.HTTPProvider('http://34.88.58.174:8546/'))

# # Адрес депозит контракта
# deposit_contract_address = '0x4242424242424242424242424242424242424242'

# # Получение ABI контракта
# deposit_contract_abi = w3_el.eth.contract(address=deposit_contract_address).abi

# print(deposit_contract_abi)


import requests

contract_address = '0x4242424242424242424242424242424242424242'
api_key = 'YOUR_API_KEY'

url = f'https://api.etherscan.io/api?module=account&action=txlist&address={contract_address}&startblock=0&endblock=99999999&sort=asc&apikey={api_key}'
response = requests.get(url)
transactions = response.json()['result']

for tx in transactions:
    print(tx)


