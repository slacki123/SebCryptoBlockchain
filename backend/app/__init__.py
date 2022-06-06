import os
import random
from time import sleep

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.app.localtunnel_app_wrapper import LocalTunnelAppRunner
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.wallet import Wallet

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': 'http://localhost:3000'}})
blockchain = Blockchain()  # Does this come from a database? Right now it's all in memory
transaction_pool = TransactionPool()
wallet = Wallet(blockchain)
peer_urls = []
my_url = []
pubsub = PubSub(blockchain, transaction_pool, peer_urls, my_url)


@app.route('/')
def route_default():
    return 'Welcome to the Blockchain Seb!'


@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())


@app.route('/blockchain/range')
def route_blockchain_range():
    # http://localhost:5000/blockchain/range?start=2&end=5
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))

    return jsonify(blockchain.to_json()[::-1][start:end])


@app.route('/blockchain/length')
def route_blockchain_length():
    return jsonify(len(blockchain.chain))


@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = transaction_pool.transaction_data()
    # Reward the miner for mining
    mining_reward = Transaction.reward_transaction(wallet)
    transaction_data.append(mining_reward.to_json())

    # add_block calls the mine method
    blockchain.add_block(transaction_data)

    resulting_block = blockchain.chain[-1]
    pubsub.broadcast_block(resulting_block)
    # After the transaction has been added to the blockchain,
    # then remove all transactions already on the blockchain from the transaction pool
    transaction_pool.clear_blockchain_transactions(blockchain)

    return jsonify(resulting_block.to_json())


@app.route('/known-addresses')
def route_known_addresses():
    known_addresses = set()

    for block in blockchain.chain:
        for transaction in block.data:
            known_addresses.update(transaction['output'].keys())

    return jsonify(list(known_addresses))


@app.route('/peer/share-url', methods=['POST'])
def route_peer_share_urls(): # Also sync chain
    peer_url = request.get_json()['peer_url']
    # Sync chain
    # All peers that are connecting should be able to see the current state of the blockchain
    result = requests.get(f'{peer_url}/blockchain')
    print(f'Result blockchain on the main APP node: {result.json()}')
    result_blockchain = Blockchain.from_json(result.json())

    # The connected peers should be able to replace the existing chain with their own chain on their own machine
    # Which is contained by the 'Blockchain' instance
    # As a result, the node that just has connected, should be synchronised with the remaining chains on the network
    try:
        blockchain.replace_chain(result_blockchain.chain)
        print(f'\n -- Successfully synced the new chain')
    except Exception as e:
        print(f'\n -- Error synchronising the new chain: {e}')

    return jsonify(blockchain.to_json())


@app.route('/peer/get-urls')
def route_peer_get_urls():
    return jsonify(peer_urls)


@app.route('/wallet/transact', methods=['POST'])
def route_wallet_transact():
    transaction_data = request.get_json()

    transaction = transaction_pool.existing_transaction(wallet.address)
    if transaction:
        transaction.update(wallet, transaction_data['recipient'], transaction_data['amount'])
    else:
        transaction = Transaction(wallet, transaction_data['recipient'], transaction_data['amount'])

    pubsub.broadcast_transaction(transaction)
    return jsonify(transaction.to_json())


@app.route('/transactions')
def route_transaction_pool():
    return jsonify(transaction_pool.transaction_data())


@app.route('/wallet/info')
def route_wallet_info():
    return jsonify({'address': wallet.address, 'balance': wallet.balance})


ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get("PEER"):
    PORT = random.randint(5001, 6000)

# Use localtunnel to create, save and broadcast your URL, so that new joined peers could use it upon connecting
# Upon broadcasting, you should receive the URL of other active peers, so that you could download their chain
local_tunnel_app_runner = LocalTunnelAppRunner(app, PORT)
local_tunnel_app_runner.run_local_tunnel_on_separate_thread()

# Broadcast new connection, even though the connection might not have been yet connected... :D
tunnel_url = local_tunnel_app_runner.tunnel_url
my_url.append(tunnel_url)
sleep(2)  # wait for localtunnel connection to be done
pubsub.broadcast_local_address(tunnel_url)

# Run the app with the specified port
local_tunnel_app_runner.run_app()
