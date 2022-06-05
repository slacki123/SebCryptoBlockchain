from backend.blockchain.block import Block


def lightning_hash(data):
    return data + "*"


class Blockchain:
    """
    Public ledger of transactions
    Implemented as a list of blocks - data sets of transactions
    """
    def __init__(self):
        self.chain: list[Block] = [Block.genesis()]

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
        serialised_chain = map(lambda block_json: Block.from_json(block_json), chain_json)
        blockchain.chain = list(serialised_chain)
        return blockchain


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

