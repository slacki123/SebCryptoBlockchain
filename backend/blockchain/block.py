import time
from backend.util.crypto_hash import crypto_hash
from backend.util.hex_to_binary import hex_to_binary
from backend.config import MINE_RATE

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}


class Block:
    """
    Unit of storage.
    Store transactions in a blockchain that supports cryptocurrency
    """
    def __init__(self, timestamp, last_hash, hash, data: list, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data: list = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return (
            'Block('
            f'{self.__dict__})'
        )

    @staticmethod
    def mine_block(last_block, data: list):
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
    def is_valid_block(last_block, block):
        """
        Validate a block by enforcing the following rules:
        1. The block must have the proper last_hash reference
        2. The block must meet the proof of work requirement - must have the proper number of leading 0's based on difficulty
        3. Difficulty must only adjust by 1 from the previous block
        4. Block hash must be a valid combination of the block fields - proves no attacker has changed the chain
        :param last_block:
        :param block:
        """

        if block.last_hash != last_block.hash:
            raise Exception("The block last_hash must be the same as the hash of the previous block!")

        if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception("The proof of work requirement was not met! Number of leading zeroes do not match difficulty")

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception("The block difficulty must only adjust by 1")

        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.nonce,
            block.difficulty
        )
        if block.hash != reconstructed_hash:
            raise Exception("The reconstructed hash is not correct!")

    def to_json(self):
        """
        Serialise the block into a dictionary of its attributes
        :return:
        """
        return self.__dict__

    @staticmethod
    def from_json(block_json):
        """
        Deserialize a block's json representation back into the instance
        :param block_json:
        :return:
        """
        return Block(**block_json)

    @staticmethod
    def genesis():
        """
        Unpack entire GENESIS_DATA dict as the genesis block
        :return: genesis Block
        """
        return Block(**GENESIS_DATA)



def main():
    genesis_block = Block.genesis()
    bad_block = Block.mine_block(genesis_block, 'bla')
    bad_block.last_hash = 'evil_data'

    Block.is_valid_block(genesis_block, bad_block)


if __name__ == '__main__':
    main()

