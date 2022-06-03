import time

from backend.blockchain.block import Block, GENESIS_DATA
from backend.config import MINE_RATE, SECONDS
from backend.util.hex_to_binary import hex_to_binary


def test_mine_block_when_genesis_block_created_then_subsequent_blocks_reference_genesis_block():
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block, data)
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
    last_block = Block(time.time_ns(), 'test_last_hash', 'test_hash', 'test_data', 4, 0)
    mined_block = Block.mine_block(last_block, 'somedata2')  # Time to compute the next hash will be very fast

    # This sometimes fails because the hex_to_binary takes more than 4 seconds sometimes
    assert mined_block.difficulty == last_block.difficulty + 1
    assert (mined_block.timestamp - last_block.timestamp) < MINE_RATE


def test_mine_block_when_slow_mining_difficulty_is_too_high_then_difficulty_is_decreased():
    # The difficulty of the added block should decrease because it will take longer than our defined MINE_RATE
    # Again, this is silly for tests, and we should be using timestamp stubs or an injectable testing config

    # Set a value > 4 for initial difficulty (number of binary preceding zeroes)
    # or it's too easy to get an initial binary value that starts with 000... which won't change difficulty
    last_block = Block(time.time_ns(), 'test_last_hash', 'test_hash', 'test_data', 4, 0)
    time.sleep(MINE_RATE / SECONDS)  # sleep for 4 sec
    mined_block = Block.mine_block(last_block, 'somedata2')  # Time to compute the next hash will be very fast

    assert mined_block.difficulty == last_block.difficulty + - 1
    assert (mined_block.timestamp - last_block.timestamp) > MINE_RATE


def test_mined_block_difficulty_is_limited_at_lowest_value_when_too_slow():
    last_block = Block(time.time_ns(), 'test_last_hash', 'test_hash', 'test_data', 1, 0)
    time.sleep(MINE_RATE / SECONDS)  # sleep for 4 sec

    mined_block = Block.mine_block(last_block, 'some_data')

    assert mined_block.difficulty == 1


def test_mined_block_time_converges_at_steady_value_related_to_mine_rate():
    pass

