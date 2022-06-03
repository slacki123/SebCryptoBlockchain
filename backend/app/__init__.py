from flask import Flask, jsonify
from backend.blockchain.blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()  # Does this come from a database? Right now it's all in memory

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

    resulting_block = blockchain.chain[-1].to_json()
    return jsonify(resulting_block)



app.run(port=5001)
