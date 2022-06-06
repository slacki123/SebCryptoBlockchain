import json

from backend.blockchain.block import Block
from backend.config import MINING_REWARD_INPUT
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


def lightning_hash(data):
    return data + "*"


class Blockchain:
    """
    Public ledger of transactions
    Implemented as a list of blocks - data sets of transactions
    """
    def __init__(self, local_chain=None, local_blockchain_file_path=None):
        self.local_blockchain_file_path = local_blockchain_file_path
        if local_chain:
            print("Loaded the chain from a local file")
        self.chain: list[Block] = local_chain or [Block.genesis()]

    def add_block(self, data: list):
        last_block = self.chain[-1]
        self.chain.append(Block.mine_block(last_block, data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    def replace_chain(self, chain):
        """
        Replace chain if the following rules apply:
        1. Incoming chain must be longer than the local one.
        2. Incoming chain must be formatted properly
        :param chain:
        :return:
        """
        if len(chain) <= len(self.chain):
            raise Exception("Cannot replace. The incoming chain must be longer")

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chain is invalid: {e}')

        # Finally, replace the current chain with the incoming chain
        self.chain = chain

    def to_json(self):
        """
        Serialise the blockchain into a list of blocks
        :return:
        """
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json):
        """
        Deserialise a list of serialised blocks into an instance of a blockchain
        The result will contain a chain list of Block instances
        :param chain_json:
        :return:
        """
        blockchain = Blockchain()
        if not chain_json:
            blockchain.chain = None
            return blockchain

        serialised_chain = map(lambda block_json: Block.from_json(block_json), chain_json)
        blockchain.chain = list(serialised_chain)
        return blockchain

    @staticmethod
    def is_valid_chain(chain: list[Block]):
        """
        Validate incoming chain
        Enforce the following rules of the blockchain
        1. Chain must start with the genesis block
        2. Blocks must be formatted correctly
        :param chain:
        """

        if chain[0].__dict__ != Block.genesis().__dict__:
            raise Exception("The genesis block must be valid")

        # Iterate over the chain blocks, except the first genesis block
        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i - 1]
            Block.is_valid_block(last_block, block)

        Blockchain.is_valid_transaction_chain(chain)

    @staticmethod
    def is_valid_transaction_chain(chain: list[Block]):
        """
        Enforce the rules of a chain composed of blocks of transactions
        1. Each transaction must only appear once in the chain
        2. There can only be one mining reward per block
        3. Each transaction must be valid

        :param chain:
        :return:
        """
        transaction_ids = set()

        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False

            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)

                if transaction.id in transaction_ids:
                    raise Exception(f'Transaction with {transaction.id} is not unique')

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception(f'There can only be one mining reward per block')
                    has_mining_reward = True
                else:
                    transaction_ids.add(transaction.id)

                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]
                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain,
                        transaction.input['address']
                    )

                    if historic_balance != transaction.input['amount']:
                        raise Exception(f'Transaction {transaction.id} has an invalid input amount')

                # Finally validate the transaction
                Transaction.is_valid_transaction(transaction)

    def save_to_file(self):
        """
        Saves existing blockchain to a file with the path specified
        """
        # write empty file if not exist
        if not self.local_blockchain_file_path:
            return

        with open(self.local_blockchain_file_path, 'w') as f:
            f.write(json.dumps(self.to_json()))




