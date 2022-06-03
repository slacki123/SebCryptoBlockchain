from backend.blockchain.block import Block


def lightning_hash(data):
    return data + "*"


class Blockchain:
    """
    Public ledger of transactions
    Implemented as a list of blocks - data sets of transactions
    """
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        last_block = self.chain[-1]
        self.chain.append(Block.mine_block(last_block, data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    @staticmethod
    def is_valid_chain(chain):
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

