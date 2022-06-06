import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec  # Elliptic curve key value pairing
from cryptography.hazmat.primitives import serialization


def retrieve_or_create_new_private_key(file_path: str) -> ec.EllipticCurvePrivateKey:
    # Return the key if it exists
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            serialised_pk = f.read()

        deserialized_pk: ec.EllipticCurvePrivateKey = serialization.load_pem_private_key(
            serialised_pk,
            None,
            default_backend()
        )
        return deserialized_pk

    # Generate new key if file does not exist
    private_key = ec.generate_private_key(  # same standard as BTC
        ec.SECP256K1(),
        default_backend()
    )
    # write to file
    pk_to_write = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(file_path, 'wb') as f:
        f.write(pk_to_write)

    return private_key
