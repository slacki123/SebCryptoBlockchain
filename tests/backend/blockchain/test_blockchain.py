from backend.blockchain.block import GENESIS_DATA, Block
from backend.blockchain.blockchain import Blockchain


def test_blockchain_first_block_is_the_same_as_genesis_block():
    blockchain = Blockchain()
    assert blockchain.chain[0].__dict__ == Block.genesis().__dict__


def test_add_block_adds_new_block_with_expected_data():
    blockchain = Blockchain()
    initial_hash = blockchain.chain[0].hash
    assert len(blockchain.chain) == 1

    data = 'test-data'
    blockchain.add_block(data)
    last_block = blockchain.chain[-1]

    assert len(blockchain.chain) == 2
    assert last_block.data == data
    assert last_block.last_hash == initial_hash
