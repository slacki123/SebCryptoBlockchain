import time

import requests
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback

from backend.blockchain.block import Block
from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool

pnconfig = PNConfiguration()
pnconfig.publish_key = "pub-c-621045a8-98b3-4c06-99a4-15c81cb782d8"
pnconfig.subscribe_key = "sub-c-41462c63-86a5-41c4-9f8d-f1829ebbae27"
pnconfig.uuid = "someuuidblablablabaoier235digfj"

CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK',
    'TRANSACTION': 'TRANSACTION',
    'NEW_CONNECTION': 'NEW_CONNECTION'
}


class Listener(SubscribeCallback):

    def __init__(self, blockchain: Blockchain, transaction_pool: TransactionPool, my_url: str):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool
        self.my_url = my_url

    def message(self, pubnub, message_object):
        print(f'\n--Channel: {message_object.channel} | Message: {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK']:
            block: dict = message_object.message
            potential_chain = self.blockchain.chain[:]  # make an exact copy of the existing blockchain list
            potential_chain.append(Block.from_json(block))  # The block must be a valid block instance

            try:
                self.blockchain.replace_chain(potential_chain)
                # Sync the transaction pool to have cleared transactions correctly
                self.transaction_pool.clear_blockchain_transactions(self.blockchain)
                self.blockchain.save_to_file()
                print('\n -- Successfully replaced the local chain')
            except Exception as e:
                print(f'\n -- Did not replace chain: {e}')

        elif message_object.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)

        elif message_object.channel == CHANNELS['NEW_CONNECTION']:
            peer_url = message_object.message
            if peer_url == self.my_url:
                return
            requests.post(f'{peer_url}/peer/sync-chain', json={'peer_url': self.my_url})


class PubSub:
    """
    Handles the publish/subscribe layer of the application.
    Provides communication between the nodes in the blockchain network
    """

    def __init__(self, blockchain: Blockchain, transaction_pool: TransactionPool, my_url: str):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transaction_pool, my_url))

    def publish(self, channel, message):
        """
        Method that takes care of publish message to the channel
        :return:
        """
        self.pubnub.publish().channel(channel).message(message).sync() # message method here is overloaded above

    def broadcast_block(self, block):
        """
        Broadcasts block to all nodes
        :param block:
        :return:
        """
        self.publish(CHANNELS['BLOCK'], block.to_json())

    def broadcast_transaction(self, transaction):
        """
        Broadcasts a transaction to all nodes
        :param transaction:
        :return:
        """
        self.publish(CHANNELS['TRANSACTION'], transaction.to_json())

    def broadcast_new_connection(self, lt_address):
        """
        Broadcasts the new connection of a new joining node
        :param lt_address:
        :return:
        """
        self.publish(CHANNELS['NEW_CONNECTION'], lt_address)


def main():
    pubsub = PubSub(Blockchain())
    time.sleep(1)

    pubsub.publish(CHANNELS['TEST'], message={'foo': 'bar'})


if __name__ == '__main__':
    main()

