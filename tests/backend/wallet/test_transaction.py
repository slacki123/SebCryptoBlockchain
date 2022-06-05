import pytest

from backend.config import STARTING_BALANCE, MINING_REWARD_INPUT, MINING_REWARD
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction


def test_transaction_when_sender_sends_amount_to_recipient_then_output_and_input_created_correctly():
    sender_wallet = Wallet()
    recipient = 'some_recipient'
    amount = 50
    transaction = Transaction(sender_wallet, recipient, amount)

    assert transaction.output[recipient] == amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount
    assert transaction.input['address'] == sender_wallet.address
    assert transaction.input['amount'] == sender_wallet.balance
    assert 'timestamp' in transaction.input
    assert transaction.input['public_key'] == sender_wallet.public_key
    assert Wallet.verify(transaction.input['public_key'], transaction.output, transaction.input['signature'])


def test_transaction_when_balance_exceeds_transaction_then_throws():
    with pytest.raises(Exception, match="Amount exceeds balance"):
        Transaction(sender_wallet=Wallet(), recipient='recipient', amount=STARTING_BALANCE + 1)


def test_transaction_update_when_balance_exceeds_transaction_amount_then_throws():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 50)

    with pytest.raises(Exception, match="Cannot update. Amount exceeds balance"):
        transaction.update(sender_wallet, 'new_recipient', STARTING_BALANCE + 1)


def test_transaction_update_when_update_values_with_multiple_recipients_valid_updates_values_correclty():
    sender_wallet = Wallet()
    first_recipient = 'first_recipient'
    first_amount = 50

    transaction = Transaction(sender_wallet, first_recipient, first_amount)

    next_recipient = 'next_recipient'
    next_amount = 76

    transaction.update(sender_wallet, next_recipient, next_amount)

    assert transaction.output[first_recipient] == first_amount
    assert transaction.output[next_recipient] == next_amount
    # The amounts to multiple recipients should be subtracted from the balance
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - first_amount - next_amount
    # test signature was updated
    assert Wallet.verify(transaction.input['public_key'], transaction.output, transaction.input['signature'])

    first_updated_again_amount = 25
    transaction.update(sender_wallet, first_recipient, first_updated_again_amount)
    total_first_recipient_amount = first_amount + first_updated_again_amount

    # Assert that multiple updates just add the amount
    assert transaction.output[first_recipient] == total_first_recipient_amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - total_first_recipient_amount - next_amount
    assert Wallet.verify(transaction.input['public_key'], transaction.output, transaction.input['signature'])


def test_is_valid_transaction_when_is_valid_does_not_throw():
    Transaction.is_valid_transaction(Transaction(Wallet(), 'recipient', 100))


def test_is_valid_transaction_when_invalid_outputs_throws_exception():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 50)
    transaction.output[sender_wallet.address] = 1000  # evil attempt to add more money to the transaction

    with pytest.raises(Exception, match="Invalid transaction output values"):
        Transaction.is_valid_transaction(transaction)


def test_is_valid_transaction_when_signature_has_been_tampered_with_then_raises_exception():
    sender_wallet = Wallet()
    some_evil_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 50)
    transaction.input['signature'] = some_evil_wallet.sign(transaction.output)

    with pytest.raises(Exception, match="Invalid transaction signature"):
        Transaction.is_valid_transaction(transaction)


def test_reward_transaction_input_and_output_are_created_correctly():
    miner_wallet = Wallet()
    transaction = Transaction.reward_transaction(miner_wallet)

    assert transaction.input == MINING_REWARD_INPUT
    assert transaction.output[miner_wallet.address] == MINING_REWARD


def test_valid_reward_transaction_when_mining_reward_transaction_does_not_raise_exception():
    reward_transaction = Transaction.reward_transaction(Wallet())
    Transaction.is_valid_transaction(reward_transaction)


def test_valid_reward_transaction_when_mining_reward_invalid_raises_exception():
    reward_transaction = Transaction.reward_transaction(Wallet())
    reward_transaction.output['extra_recipient'] = 20

    with pytest.raises(Exception, match="Invalid mining reward"):
        Transaction.is_valid_transaction(reward_transaction)


def test_valid_reward_transaction_when_mining_reward_amount_invalid_raises_exception():
    miner_wallet = Wallet()
    reward_transaction = Transaction.reward_transaction(miner_wallet)
    reward_transaction.output[miner_wallet] = 9000

    with pytest.raises(Exception, match="Invalid mining reward"):
        Transaction.is_valid_transaction(reward_transaction)



