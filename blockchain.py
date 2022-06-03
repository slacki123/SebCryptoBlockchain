from block import Block


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

