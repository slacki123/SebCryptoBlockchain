from backend.blockchain.block import Block, GENESIS_DATA


def test_mine_block_when_genesis_block_created_then_subsequent_blocks_reference_genesis_block():
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block, data)
    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    # Assert the hash starts with the number of zeros that is same as the difficulty
    assert block.hash[0:block.difficulty] == block.difficulty * '0'


def test_genesis_returns_a_block_type_with_expected_values():
    gen_block = Block.genesis()
    assert isinstance(gen_block, Block)
    for key, value in GENESIS_DATA.items():
        assert getattr(gen_block, key) == value
