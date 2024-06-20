from web3 import Web3
from eth_account.messages import encode_defunct

# Подключение к Ethereum ноде
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/your_infura_project_id'))

# Адрес смарт-контракта для отслеживания депозитов
contract_address = '0x4242424242424242424242424242424242424242'

# Адрес смарт-контракта для вызова методов
contract_address_validator = '0xe048ac2464c8028ecc8c931b70b11e20fd0a5318'

# Аби для смарт-контракта
contract_abi = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes","name":"pubkey","type":"bytes"}],"name":"AlreadyExists","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"}],"name":"WrongSignature","type":"event"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"pubkey","type":"bytes"}],"name":"alreadyExists","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"}],"name":"invalidSignature","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

# Создание объекта смарт-контракта
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Функция для проверки подписи
def is_signature_valid(message, signature, sender):
    # Преобразование сообщения в хэш
    message_hash = Web3.keccak(text=message)
    # Проверка подписи
    try:
        recovered_address = web3.eth.account.recover_message(encode_defunct(text=message), signature=signature)
        return sender.lower() == recovered_address.lower()
    except:
        return False

# Функция для вызова метода invalidSignature
def call_invalid_signature():
    # Вызов метода invalidSignature
    tx_hash = contract.functions.invalidSignature().transact()
    # Ожидание подтверждения транзакции
    web3.eth.waitForTransactionReceipt(tx_hash)

# Функция для вызова метода alreadyExists
def call_already_exists(public_key):
    # Вызов метода alreadyExists
    tx_hash = contract.functions.alreadyExists(public_key).transact()
    # Ожидание подтверждения транзакции
    web3.eth.waitForTransactionReceipt(tx_hash)

# Функция для проверки наличия валидатора на Consensus Layer
def validator_already_exists(public_key):
    try:
        # Создание объекта смарт-контракта для работы с адресом contract_address_validator
        contract_validator = web3.eth.contract(address=contract_address_validator, abi=contract_abi)
        
        # Вызов метода для проверки наличия валидатора на Consensus Layer
        exists = contract_validator.functions.validatorExists(public_key).call()
        return exists
    except Exception as e:
        print(f"Ошибка при проверке наличия валидатора: {str(e)}")
        return False

# Отслеживание новых транзакций на контракт
def watch_deposits():
    filter = contract.events.Deposit.createFilter(fromBlock='latest')
    for event in filter.get_new_entries():
        # Получение данных о транзакции
        transaction = web3.eth.getTransaction(event['transactionHash'])
        # Проверка подписи
        if is_signature_valid(event['message'], event['signature'], transaction['from']):
            # Проверка наличия валидатора на Consensus Layer
            if validator_already_exists(event['publicKey']):
                # Вызов метода alreadyExists
                call_already_exists(event['publicKey'])
        else:
            # Вызов метода invalidSignature
            call_invalid_signature()

# Основной цикл программы
if __name__ == '__main__':
    watch_deposits()