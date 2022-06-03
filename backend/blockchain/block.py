import time
from backend.util.crypto_hash import crypto_hash
from backend.util.hex_to_binary import hex_to_binary
from backend.config import MINE_RATE

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': 'genesis_data',
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}


class Block:
    """
    Unit of storage.
    Store transactions in a blockchain that supports cryptocurrency
    """
    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return (
            'Block('
            f'{self.__dict__})'
        )

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and data. Until a block hash is found that meets
        the leading 0's proof of work requirement
        :param last_block: needed to retrieve last hash
        :param data: data of the block
        :return: a new block
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = last_block.difficulty
        nonce = 0  # nonce is just a one time number that we will modify to get the hash result we require
        hash = crypto_hash(timestamp, last_hash, difficulty, nonce)

        # Algorithm checking the number of leading zeros is the same as the difficulty number
        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()  # doesn't the timestamp here make the mining a bit more difficult?
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            # reassign the hash and repeat the process until we find the number of 0's required
            hash = crypto_hash(timestamp, last_hash, difficulty, nonce)

        # Return the new block with the adjusted difficulty, correspondingly adjusted hash, and other values
        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculate the adjusted difficulty based on the MINE_RATE.
        Increase difficulty if blocks are mined too quickly
        Decrease difficulty if blocks are mined too slowly
        :param last_block:
        :param new_timestamp:
        :return:
        """

        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        return last_block.difficulty - 1 if last_block.difficulty > 1 else 1  # ensure this value does not go negative

    @staticmethod
    def genesis():
        """
        Unpack entire GENESIS_DATA dict as the genesis block
        :return: genesis Block
        """
        return Block(**GENESIS_DATA)


def main():
    last_block = Block.genesis()
    block = Block.mine_block(last_block, 'somedata')
    print(block)


if __name__ == '__main__':
    main()

