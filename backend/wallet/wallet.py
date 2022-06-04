import json
import uuid

from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec  # Elliptic curve key value pairing
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


class Wallet:
    """
    The wallet for a miner in the system.
    Keeps track of the miner's balance.
    Allows the miner to authorise transactions via signatures
    """
    def __init__(self):
        self.address: str = str(uuid.uuid4())[0:8]  # Get only 8 characters of the UUID
        self.balance = STARTING_BALANCE
        self.private_key: ec.EllipticCurvePrivateKey = ec.generate_private_key( # same standard as BTC
            ec.SECP256K1(),
            default_backend()
        )  # same standard as BTC
        self.public_key: ec.EllipticCurvePublicKey = self.private_key.public_key()

    def sign(self, data):
        """
        Generate signature based on the local private key
        :param data:
        :return: signed object with the local privvate key
        """
        encoded_data = json.dumps(data).encode('utf-8')
        return self.private_key.sign(encoded_data, ec.ECDSA(hashes.SHA256()))  # Elliptic curve signing algorithm

    @staticmethod
    def verify(public_key: ec.EllipticCurvePublicKey, data: any, signature: bytes) -> bool:
        """
        Verify a signature based on the original public key
        :param public_key:
        :param data:
        :param signature:
        :return:
        """
        encoded_data = json.dumps(data).encode('utf-8')
        sha_256_hash = ec.ECDSA(hashes.SHA256())
        try:
            public_key.verify(signature, encoded_data, sha_256_hash)
            return True
        except InvalidSignature as e:
            return False


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
