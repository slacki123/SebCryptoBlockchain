import time
from crypto_hash import crypto_hash

class Block:
    """
    Unit of storage.
    Store transactions in a blockchain that supports cryptocurrency
    """
    def __init__(self, timestamp, last_hash, hash, data):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data

    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}'
            ')'
        )

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and data. Only needs data and last block to mine
        :param last_block: needed to retrieve last hash
        :param data: data of the block
        :return: a new block
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        hash = crypto_hash(timestamp, last_hash)
        return Block(timestamp, last_hash, hash, data)

    @staticmethod
    def genesis():
        """
        Generate the genesis block
        :return: genesis Block
        """

        return Block(1, 'genesis_last', 'genesis_hash', 'genesis_data')


def main():
    last_block = Block.genesis()
    block = Block.mine_block(last_block, 'somedata')
    print(block)


if __name__ == '__main__':
    main()

