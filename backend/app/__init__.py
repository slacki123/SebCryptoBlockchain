import os
import random

import requests
from flask import Flask, jsonify
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub

app = Flask(__name__)
blockchain = Blockchain()  # Does this come from a database? Right now it's all in memory
pubsub = PubSub(blockchain)

@app.route('/')
def route_default():
    return 'Welcome to the Blockchain Seb!'


@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())


@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = 'stubbed_transaction_data'

    # add_block calls the mine method
    blockchain.add_block(transaction_data)

    resulting_block = blockchain.chain[-1]
    pubsub.broadcast_block(resulting_block)

    return jsonify(resulting_block.to_json())


ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get("PEER"):
    PORT = random.randint(5001, 6000)

    # All peers that are connecting should be able to see the current state of the blockchain
    result = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    print(f'Result: {result.json()}')
    result_blockchain = Blockchain.from_json(result.json())

    try:
        blockchain.replace_chain(result_blockchain)
        print(f'\n -- Successfully synced the new chain')
    except Exception as e:
        print(f'\n -- Error synchronising the new chain: {e}')

app.run(port=PORT)
