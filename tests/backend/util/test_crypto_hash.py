from backend.util.crypto_hash import crypto_hash


def test_crypto_hash_when_arguments_out_of_order_then_still_creates_same_hash():
    assert crypto_hash(1, [2], 3) == crypto_hash([2], 1, 3)


def test_crypto_hash_when_input_data_type_varies_then_hashes_correctly_as_string():
    test_hash = crypto_hash(1, "2", ["bla"])
    assert len(test_hash) > 0
    assert type(test_hash) == str


def test_crypto_hash_when_single_input_then_hashes_correctly():
    test_hash = crypto_hash("bla")
    assert len(test_hash) > 0
    assert type(test_hash) == str
