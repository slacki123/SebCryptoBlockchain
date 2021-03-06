import json
import os
import uuid

from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec  # Elliptic curve key value pairing
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

from backend.util.crypto_hash import crypto_hash


class Wallet:
    """
    The wallet for a miner in the system.
    Keeps track of the miner's balance.
    Allows the miner to authorise transactions via signatures
    """

    def __init__(self, blockchain=None, private_key=None):
        self.blockchain = blockchain
        self.private_key: ec.EllipticCurvePrivateKey = private_key or ec.generate_private_key( # same standard as BTC
            ec.SECP256K1(),
            default_backend()
        )  # same standard as BTC
        self.public_key: str = self.serialize_public_key()
        self.address: str = crypto_hash(self.serialize_public_key())  # Create the address from the hashed public key

    @property
    def balance(self):
        return Wallet.calculate_balance(self.blockchain, self.address)

    def sign(self, data):
        """
        Generate signature based on the local private key
        :param data:
        :return: signed object with the local privvate key
        """
        encoded_data = json.dumps(data).encode('utf-8')
        private_key = self.private_key.sign(encoded_data, ec.ECDSA(hashes.SHA256()))  # Elliptic curve signing algorithm
        return decode_dss_signature(private_key)

    def serialize_public_key(self):
        """
        Reset the public key to it's serialized version so that it is jsonable
        :return:
        """
        public_key = self.private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
        return public_key

    @staticmethod
    def verify(public_key: str, data: any, signature: tuple[int, int]) -> bool:
        """
        Verify a signature based on the original public key
        :param public_key:
        :param data:
        :param signature:
        :return:
        """
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )
        (r, s) = signature # elliptic curve coordinates
        encoded_signature = encode_dss_signature(r, s)

        encoded_data = json.dumps(data).encode('utf-8')
        sha_256_hash = ec.ECDSA(hashes.SHA256())
        try:
            deserialized_public_key.verify(encoded_signature, encoded_data, sha_256_hash)
            return True
        except InvalidSignature as e:
            return False

    @staticmethod
    def calculate_balance(blockchain, address: str):
        """
        Calculate the balance of a wallet address, based on the data on the blockchain.

        The balance is found by adding the output values that belong to the address since the most recent transaction
        by that address
        :param blockchain:
        :param address:
        :return:
        """
        balance = STARTING_BALANCE

        # If blockchain is empty, just return balance
        if not blockchain:
            return balance

        for block in blockchain.chain:
            for transaction in block.data:
                if transaction['input']['address'] == address:
                    # any time the address conducts any transactions, it resets its balance
                    balance = transaction['output'][address]
                    # any time the address conducts any transactions, subtract its differences of remaining balances
                    # balance = balance - (STARTING_BALANCE - transaction['output'][address])
                elif address in transaction['output']:
                    # If the recipient is receiving an amount, then add it to the balance
                    balance += transaction['output'][address]
        return balance


def main():
    wallet = Wallet()
    print(f'Wallet dict: {wallet.__dict__}')

    data = {'foo': 'bar'}
    signed_data = wallet.sign(data)
    print(f'Signed data: {signed_data}')

    should_be_valid = wallet.verify(wallet.public_key, data, signed_data)
    print(f'Should be valid: {should_be_valid}')

    should_be_invalid = wallet.verify(Wallet().public_key, data, signed_data)
    print(f'Should be invalid: {should_be_invalid}')


if __name__ == '__main__':
    main()
