from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


def test_set_transaction():
    transaction_pool = TransactionPool()
    wallet = Wallet()
    transaction = Transaction(wallet, 'recipient', 1)

    transaction_pool.set_transaction(transaction)

    assert transaction_pool.transaction_map[transaction.id] == transaction


def test_clear_blockchain_transactions():
    transaction1 = Transaction(Wallet(), 'recipient', 1)
    transaction2 = Transaction(Wallet(), 'recipient', 2)

    transaction_pool = TransactionPool()
    transaction_pool.set_transaction(transaction1)
    transaction_pool.set_transaction(transaction2)

    blockchain = Blockchain()
    blockchain.add_block([transaction1.to_json(), transaction2.to_json()])

    assert len(blockchain.chain) == 2
    assert transaction1.id in transaction_pool.transaction_map
    assert transaction2.id in transaction_pool.transaction_map

    transaction_pool.clear_blockchain_transactions(blockchain)

    assert len(blockchain.chain) == 2
    assert transaction1.id not in transaction_pool.transaction_map
    assert transaction2.id not in transaction_pool.transaction_map





