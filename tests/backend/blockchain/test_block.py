import time

import pytest

from backend.blockchain.block import Block, GENESIS_DATA
from backend.config import MINE_RATE, SECONDS
from backend.util.hex_to_binary import hex_to_binary


def test_mine_block_when_genesis_block_created_then_subsequent_blocks_reference_genesis_block():
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block, [data])
    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    # Assert the hash starts with the number of zeros that is same as the difficulty
    assert hex_to_binary(block.hash)[0:block.difficulty] == block.difficulty * '0'


def test_genesis_returns_a_block_type_with_expected_values():
    gen_block = Block.genesis()
    assert isinstance(gen_block, Block)
    for key, value in GENESIS_DATA.items():
        assert getattr(gen_block, key) == value


def test_mine_block_when_quick_mining_difficulty_is_too_low_then_difficulty_is_increased():
    # The difficulty of the added block should increase because of our config having a high value for MINE_RATE,
    # If the config is changed, test might break
    # We should be used timestamp stubs, or test config, but whatever. This is for the course purposes

    # Set a value > 4 for initial difficulty (number of binary preceding zeroes)
    # or it's too easy to get an initial binary value that starts with 000... which won't change difficulty
    last_block = Block(time.time_ns(), 'test_last_hash', 'test_hash', ['test_data'], 5, 0)
    mined_block = Block.mine_block(last_block, ['somedata2'])  # Time to compute the next hash will be very fast

    # This sometimes fails because the hex_to_binary takes more than 4 seconds sometimes
    assert mined_block.difficulty == last_block.difficulty + 1
    assert (mined_block.timestamp - last_block.timestamp) < MINE_RATE


def test_mine_block_when_slow_mining_difficulty_is_too_high_then_difficulty_is_decreased():
    # The difficulty of the added block should decrease because it will take longer than our defined MINE_RATE
    # Again, this is silly for tests, and we should be using timestamp stubs or an injectable testing config

    # Set a value > 4 for initial difficulty (number of binary preceding zeroes)
    # or it's too easy to get an initial binary value that starts with 000... which won't change difficulty
    last_block = Block(time.time_ns(), 'test_last_hash', 'test_hash', ['test_data'], 5, 0)
    time.sleep(MINE_RATE / SECONDS)  # sleep for 4 sec
    mined_block = Block.mine_block(last_block, ['somedata2'])  # Time to compute the next hash will be very fast

    assert mined_block.difficulty == last_block.difficulty + - 1
    assert (mined_block.timestamp - last_block.timestamp) > MINE_RATE


def test_mined_block_difficulty_is_limited_at_lowest_value_when_too_slow():
    last_block = Block(time.time_ns(), 'test_last_hash', 'test_hash', ['test_data'], 1, 0)
    time.sleep(MINE_RATE / SECONDS)  # sleep for 4 sec

    mined_block = Block.mine_block(last_block, ['some_data'])

    assert mined_block.difficulty == 1


def test_mined_block_time_converges_at_steady_value_related_to_mine_rate():
    pass


def test_is_valid_block_when_block_is_valid_does_not_throw():
    last_block = Block.genesis()
    block = Block.mine_block(last_block, ['test_data'])
    Block.is_valid_block(last_block, block)


def test_is_valid_block_when_block_last_hash_is_invalid_then_throws():
    last_block = Block.genesis()
    block = Block.mine_block(last_block, ['test_data'])
    block.last_hash = 'evil_last_hash'

    with pytest.raises(Exception, match="The block last_hash must be the same as the hash of the previous block!"):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_when_block_hash_is_incorrectly_constructed_then_throws():
    last_block = Block.genesis()
    block = Block.mine_block(last_block, ['test_data'])
    block.nonce = 'some_evil_nonce'

    with pytest.raises(Exception, match="The reconstructed hash is not correct!"):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_when_block_hash_is_incorrect_then_throws():
    last_block = Block.genesis()
    block = Block.mine_block(last_block, ['test_data'])
    block.hash = '0000000001234bbbaaa'

    with pytest.raises(Exception, match="The reconstructed hash is not correct!"):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_proof_of_work_requirement_not_met_then_throws():
    last_block = Block.genesis()
    block = Block.mine_block(last_block, ['test_data'])
    block.hash = 'fff'

    with pytest.raises(Exception, match="The proof of work requirement was not met.*"):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_when_difficulty_is_not_adjusted_by_1_then_throws():
    last_block = Block.genesis()
    block = Block.mine_block(last_block, ['test_data'])
    jumped_difficulty = 10
    block.hash = f'{"0" * (jumped_difficulty + last_block.difficulty)}'
    block.difficulty = last_block.difficulty + jumped_difficulty

    with pytest.raises(Exception, match="The block difficulty must only adjust by 1"):
        Block.is_valid_block(last_block, block)


