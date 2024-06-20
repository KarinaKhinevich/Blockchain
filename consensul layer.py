from web3 import Web3
from eth_account.messages import encode_defunct

# Connection to  Ethereum node
web3 = Web3(Web3.HTTPProvider(''))

# Deposit-contract address
contract_address = ''

# Smart-contract address
contract_address_validator = ''

# Smart-contract abi
contract_abi = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes","name":"pubkey","type":"bytes"}],"name":"AlreadyExists","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"}],"name":"WrongSignature","type":"event"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"pubkey","type":"bytes"}],"name":"alreadyExists","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"}],"name":"invalidSignature","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

# Creating smart-contract object
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Function to check signatures
def is_signature_valid(message, signature, sender):
    # Converting message into hash
    message_hash = Web3.keccak(text=message)
    # Checking signature
    try:
        recovered_address = web3.eth.account.recover_message(encode_defunct(text=message), signature=signature)
        return sender.lower() == recovered_address.lower()
    except:
        return False

# Function to call a smart-contracts method <invalidSignature>
def call_invalid_signature():
    # Вызов метода invalidSignature
    tx_hash = contract.functions.invalidSignature().transact()
    # Waiting for transaction confirmation
    web3.eth.waitForTransactionReceipt(tx_hash)

# Function to call a smart-contracts method  <alreadyExists>
def call_already_exists(public_key):
    # Calling alreadyExists method
    tx_hash = contract.functions.alreadyExists(public_key).transact()
    # Waiting for transaction confirmation
    web3.eth.waitForTransactionReceipt(tx_hash)

# Function to check validator on Consensus Layer
def validator_already_exists(public_key):
    try:
        # Create a smart contract object to work with the contract_address_validator address
        contract_validator = web3.eth.contract(address=contract_address_validator, abi=contract_abi)
        
        # Method for checking the presence of validator on Consensus Layer
        exists = contract_validator.functions.validatorExists(public_key).call()
        return exists
    except Exception as e:
        print(f"The validation check failed: {str(e)}")
        return False

# Tracking new contract transactions
def watch_deposits():
    filter = contract.events.Deposit.createFilter(fromBlock='latest')
    for event in filter.get_new_entries():
        # Transaction data retrieval
        transaction = web3.eth.getTransaction(event['transactionHash'])
        # Signature verification
        if is_signature_valid(event['message'], event['signature'], transaction['from']):
            # Validator check on Consensus Layer
            if validator_already_exists(event['publicKey']):
                # Calling alreadyExists method
                call_already_exists(event['publicKey'])
        else:
            # Calling invalidSignature method
            call_invalid_signature()

# Main program cycle
if __name__ == '__main__':
    watch_deposits()
