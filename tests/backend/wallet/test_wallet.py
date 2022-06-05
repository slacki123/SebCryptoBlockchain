from backend.blockchain.blockchain import Blockchain
from backend.config import STARTING_BALANCE
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


def test_verify_valid_signature_returns_true():
    data = {'foo': 'test_data'}
    wallet = Wallet()
    signature = wallet.sign(data)
    assert Wallet.verify(wallet.public_key, data, signature)

    
def test_verify_valid_signature_returns_false():
    data = {'foo': 'test_data'}
    wallet = Wallet()
    signature = wallet.sign(data)
    assert not Wallet.verify(Wallet().public_key, data, signature)


def test_calculate_wallet_balance_when_no_transactions_balance_equals_starting_balance():
    blockchain = Blockchain()
    wallet = Wallet()

    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE


def test_calculate_wallet_balance_when_transaction_made_then_wallet_balance_updated_according_to_amount_spent():
    blockchain = Blockchain()
    wallet = Wallet()
    amount = 50
    transaction = Transaction(wallet, 'recipient', amount)
    blockchain.add_block([transaction.to_json()])

    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE - amount


def test_calculate_wallet_balance_when_received_amounts_from_multiple_wallets_then_balance_updated_correctly_for_all():
    blockchain = Blockchain()
    sending_wallet1 = Wallet()
    sending_wallet2 = Wallet()
    receiving_wallet1 = Wallet()

    received_amount1 = 14
    transaction1 = Transaction(sending_wallet1, receiving_wallet1.address, received_amount1)

    received_amount2 = 16
    transaction2 = Transaction(sending_wallet2, receiving_wallet1.address, received_amount2)

    blockchain.add_block([transaction1.to_json(), transaction2.to_json()])

    # Sender 1 has an amount deducted
    assert Wallet.calculate_balance(blockchain, sending_wallet1.address) == STARTING_BALANCE - received_amount1
    # Sender 2 has an amount deducted
    assert Wallet.calculate_balance(blockchain, sending_wallet2.address) == STARTING_BALANCE - received_amount2
    # Sender 3 has the amounts of sender 1 and 2 added
    assert Wallet.calculate_balance(blockchain, receiving_wallet1.address) == \
           STARTING_BALANCE + received_amount1 + received_amount2


def test_calculate_wallet_balance_when_received_amounts_from_multiple_wallets_as_multiple_blocks_then_balance_updated_correctly_for_all():
    blockchain = Blockchain()
    sending_wallet1 = Wallet()
    sending_wallet2 = Wallet()
    receiving_wallet1 = Wallet()

    received_amount1 = 14
    transaction1 = Transaction(sending_wallet1, receiving_wallet1.address, received_amount1)

    received_amount2 = 16
    transaction2 = Transaction(sending_wallet2, receiving_wallet1.address, received_amount2)

    blockchain.add_block([transaction1.to_json()])
    blockchain.add_block([transaction2.to_json()])

    # Sender 1 has an amount deducted
    assert Wallet.calculate_balance(blockchain, sending_wallet1.address) == STARTING_BALANCE - received_amount1
    # Sender 2 has an amount deducted
    assert Wallet.calculate_balance(blockchain, sending_wallet2.address) == STARTING_BALANCE - received_amount2
    # Sender 3 has the amounts of sender 1 and 2 added
    assert Wallet.calculate_balance(blockchain, receiving_wallet1.address) == \
           STARTING_BALANCE + received_amount1 + received_amount2


def test_calculate_wallet_balance_when_sent_amounts_to_multiple_wallets_then_balance_updated_correctly_for_all():
    blockchain = Blockchain()
    sending_wallet1 = Wallet()
    receiving_wallet1 = Wallet()
    receiving_wallet2 = Wallet()

    sent_amount1 = 14
    transaction1 = Transaction(sending_wallet1, receiving_wallet1.address, sent_amount1)

    sent_amount2 = 16
    transaction2 = Transaction(sending_wallet1, receiving_wallet2.address, sent_amount2)

    blockchain.add_block([transaction1.to_json(), transaction2.to_json()])

    sent_amount1 = 14
    transaction1 = Transaction(sending_wallet1, receiving_wallet1.address, sent_amount1)

    sent_amount2 = 16
    transaction2 = Transaction(sending_wallet1, receiving_wallet2.address, sent_amount2)

    blockchain.add_block([transaction1.to_json(), transaction2.to_json()])

    # Sender 1 has an amount deducted based on what was sent to receiver 1 and 2
    assert Wallet.calculate_balance(blockchain, sending_wallet1.address) == STARTING_BALANCE - sent_amount1 - sent_amount2
    # Receiver 1 has amount added
    assert Wallet.calculate_balance(blockchain, receiving_wallet1.address) == STARTING_BALANCE + sent_amount1
    # Receiver 2 has amount added
    assert Wallet.calculate_balance(blockchain, receiving_wallet2.address) == STARTING_BALANCE + sent_amount2







