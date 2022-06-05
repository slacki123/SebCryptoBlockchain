import requests
import time

from backend.wallet.wallet import Wallet

BASE_URL = 'http://localhost:5000'


def get_blockchain():
    return requests.get(f'{BASE_URL}/blockchain').json()


def get_blockchain_mine():
    return requests.get(f'{BASE_URL}/blockchain/mine').json()


def post_wallet_transactions(recipient, amount):
    return requests.post(
        f'{BASE_URL}/wallet/transact',
        json={'recipient': recipient, 'amount': amount}
    ).json()


start_blockchain = get_blockchain()
print(f'start_blockchain: {start_blockchain}')

recipient = Wallet().address
post_wallet_transact1 = post_wallet_transactions(recipient, 42)
print(f'\npost_wallet_transact1: {post_wallet_transact1}')

time.sleep(1)
post_wallet_transact2 = post_wallet_transactions(recipient, 18)
print(f'\npost_wallet_transact2: {post_wallet_transact2}')

# In the future, use async...
time.sleep(1)
mined_block = get_blockchain_mine()
print(f'\nmined_block: {mined_block}')
