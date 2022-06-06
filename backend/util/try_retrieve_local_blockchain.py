import json
import os

from backend.blockchain.blockchain import Blockchain


def try_retrieve_local_blockchain(file_path) -> Blockchain:
    if not file_path:
        return Blockchain()

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            result_text = f.read()
            resulting_blockchain = json.loads(result_text) if result_text else None
            return Blockchain.from_json(resulting_blockchain)

    return Blockchain()




