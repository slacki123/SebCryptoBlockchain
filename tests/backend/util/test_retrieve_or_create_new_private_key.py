import os

from backend.util.retrieve_or_generate_private_key import retrieve_or_create_new_private_key
from cryptography.hazmat.primitives import serialization

file_path = "test_pk_file_path.txt"


def test_create_new_key_when_not_exists_creates_new():
    # Clean the file
    if os.path.exists(file_path):
        os.remove(file_path)

    # Make sure doesn't exist
    assert not os.path.exists(file_path)
    key = retrieve_or_create_new_private_key(file_path)
    # assert it exists
    assert os.path.exists(file_path)
    assert key
    # remove at the end
    os.remove(file_path)


def test_create_new_key_when_exists_then_returns_value():
    test_private_key = retrieve_or_create_new_private_key(file_path)
    assert os.path.exists(file_path)
    assert test_private_key
    # Assert contents are the same
    retrieved_key_bytes = test_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open(file_path, 'rb') as f:
        test_private_key_from_file_bytes = f.read()
    assert test_private_key_from_file_bytes
    assert retrieved_key_bytes == test_private_key_from_file_bytes

    # remove at the end
    os.remove(file_path)



