import pytest

from backend.util.crypto_hash import crypto_hash
from backend.util.hex_to_binary import hex_to_binary


def test_hex_to_binary():
    for i in range(256):
        hex_number = hex(i)[2:]
        binary_number = hex_to_binary(hex_number)

        # convert  binary back to int
        original_number = int(binary_number, 2)

        assert i == original_number

