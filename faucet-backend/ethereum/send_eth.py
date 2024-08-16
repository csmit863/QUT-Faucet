from web3 import Web3, HTTPProvider, Account
from web3.exceptions import TransactionNotFound, BadFunctionCallOutput
from main import send_email
import os, dotenv


dotenv.load_dotenv()
web3_instance = Web3(HTTPProvider(os.environ.get('web3_provider')))
private_key = os.environ.get('faucet_key')
faucet_account = Account.from_key(private_key)
faucet_manager = os.environ.get('faucet_manager')
eth_distribution_amount = int(0.452*10**18)
print('Connected to Blockchain: ', web3_instance.is_connected())

async def check_balance():
    # check the balance of the faucet wallet which is in use (effectively a hot wallet)
    # ping the managers of the server when the balance hits a certain low number
    balance_low_threshold = 10*10**18 # 10 test ether
    print(faucet_account.address)
    faucet_balance = web3_instance.eth.get_balance(faucet_account.address)
    print('faucet balance',faucet_balance)
    print('balance low threshold', balance_low_threshold)
    if faucet_balance < balance_low_threshold:
        send_email(faucet_manager, f"top up eth faucet! \n balance: {faucet_balance}", 'QUT ETH Faucet Balance Low')
        print('ping sent to faucet manager')
        return faucet_balance
    else:
        return faucet_balance
    


async def send_eth(address):
    # check there is enough to send before attempting, if not, return an error message
    balance = await check_balance()
    nonce = web3_instance.eth.get_transaction_count(faucet_account.address)
    if balance > eth_distribution_amount:
        try:
            tx = {
                'nonce': nonce,
                'to': address,
                'value': eth_distribution_amount,
                'gas': 200000,
                'gasPrice': web3_instance.to_wei(50, 'gwei')
            }
            signed_tx = web3_instance.eth.account.sign_transaction(tx, private_key)
            tx_hash = web3_instance.eth.send_raw_transaction(signed_tx.rawTransaction)
            status = 'success'
            return status, tx_hash.hex()
        except (TransactionNotFound, BadFunctionCallOutput) as e:
            print(f'Transaction error: {e}')
            status = 'error'
            return status, None
        except Exception as e:
            print(f'Unexpected error: {e}')
            status = 'error'
            return status, None
    else:
        status = 'error: faucet running dry (not enough funds to send)'
        return status

