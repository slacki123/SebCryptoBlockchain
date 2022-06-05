import pytest

from backend.blockchain.block import GENESIS_DATA, Block
from backend.blockchain.blockchain import Blockchain


def test_blockchain_first_block_is_the_same_as_genesis_block():
    blockchain = Blockchain()
    assert blockchain.chain[0].__dict__ == Block.genesis().__dict__


def test_add_block_adds_new_block_with_expected_data():
    blockchain = Blockchain()
    initial_hash = blockchain.chain[0].hash
    assert len(blockchain.chain) == 1

    data = ['test-data']
    blockchain.add_block(data)
    last_block = blockchain.chain[-1]

    assert len(blockchain.chain) == 2
    assert last_block.data == data
    assert last_block.last_hash == initial_hash


@pytest.fixture
def blockchain_three_blocks():
    blockchain = Blockchain()

    for i in range(3):
        blockchain.add_block([i])

    return blockchain


def test_is_valid_chain_when_all_blocks_valid_then_does_not_throw(blockchain_three_blocks):
    Blockchain.is_valid_chain(blockchain_three_blocks.chain)


def test_is_valid_chain_when_genesis_block_invalid_then_throws(blockchain_three_blocks):
    blockchain_three_blocks.chain[0].hash = 'some_evil_hash'

    with pytest.raises(Exception, match='The genesis block must be valid'):
        Blockchain.is_valid_chain(blockchain_three_blocks.chain)


def test_is_valid_chain_when_last_block_is_invalid_then_throws(blockchain_three_blocks):
    blockchain_three_blocks.chain[-1].nonce = 'some_evil_nonce'

    with pytest.raises(Exception, match='The reconstructed hash is not correct!'):
        Blockchain.is_valid_chain(blockchain_three_blocks.chain)


def test_is_valid_chain_when_all_blocks_are_invalid_then_throws(blockchain_three_blocks):
    for i in range(1, len(blockchain_three_blocks.chain)):
        blockchain_three_blocks.chain[i].nonce = "some_evil_nonce"

    with pytest.raises(Exception, match='The reconstructed hash is not correct!'):
        Blockchain.is_valid_chain(blockchain_three_blocks.chain)


def test_replace_chain_when_chain_valid_then_replaces_correctly(blockchain_three_blocks):
    current_blockchain = Blockchain()
    current_blockchain.replace_chain(blockchain_three_blocks.chain)

    assert current_blockchain.chain == blockchain_three_blocks.chain


def test_replace_chain_when_incoming_chain_is_shorter_then_throws(blockchain_three_blocks):
    new_incoming_chain = Blockchain()

    with pytest.raises(Exception, match="The incoming chain must be longer"):
        blockchain_three_blocks.replace_chain(new_incoming_chain.chain)


def test_replace_chain_when_chain_is_invalid_then_throws(blockchain_three_blocks):
    blockchain = Blockchain()
    blockchain_three_blocks.chain[1].hash = 'evil_hash'

    with pytest.raises(Exception, match='The incoming chain is invalid'):
        blockchain.replace_chain(blockchain_three_blocks.chain)


