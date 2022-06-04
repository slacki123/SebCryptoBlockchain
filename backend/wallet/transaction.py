import time
import uuid

from backend.wallet.wallet import Wallet


class Transaction:
    """
    Document of an exchange of currency, from a sender to one or more recipients
    """

    def __init__(  # terrible none assignment
            self,
            sender_wallet: Wallet = None,
            recipient=None,
            amount=None,
            id=None,
            output=None,
            input=None
    ):
        self.id = id or str(uuid.uuid4())[0:8]
        self.output = output or self.create_output(
            sender_wallet,
            recipient,
            amount
        )
        self.input = input or self.create_input(sender_wallet, self.output)

    @staticmethod
    def create_output(sender_wallet: Wallet, recipient, amount) -> dict:
        """
        structure output data for the transaction
        This the resulting balance that the sender will have after the transaction, and the amount recipient receives
        Output name is a bit misleading. This is the output of the resulting values after the transaction only
        :param recipient: Recipient the money is going to
        :param sender_wallet: the user sending the money
        :param amount: amount being sent
        :return:
        """
        if amount > sender_wallet.balance:
            raise Exception("Amount exceeds balance")

        output = {
            recipient: amount,
            sender_wallet.address: sender_wallet.balance - amount
        }

        return output

    @staticmethod
    def create_input(sender_wallet: Wallet, output: dict) -> dict:
        """
        structure input data for the transaction
        Sign the transaction and include sender's public key and address
        Input name might be misleading, but it is the signed input that will go into the blockchain.
        :param sender_wallet:
        :param output: Is the actual transactional data
        :return:
        """
        return {
            'timestamp': time.time_ns(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(output)
        }

    def update(self, sender_wallet: Wallet, recipient, amount: float):
        """
        Update the transaction with an existing or new recipient
        :param sender_wallet:
        :param recipient:
        :param amount:
        :return:
        """
        if amount > self.output[sender_wallet.address]:
            raise Exception("Cannot update. Amount exceeds balance")
        if recipient in self.output:
            self.output[recipient] = self.output[recipient] + amount  # update existing amount to be sent to recipient
        else:
            self.output[recipient] = amount  # add the new address and assign an amount

        # Update the new balance of the sender after the transaction has been made
        self.output[sender_wallet.address] = self.output[sender_wallet.address] - amount

        # Update the signed input that will go onto the blockchain
        self.input = self.create_input(sender_wallet, self.output)

    @staticmethod
    def is_valid_transaction(transaction):
        """
        Validate a transaction
        Raise exception if transaction is invalid
        :param transaction:
        :raise: Exception
        """
        output_total = sum(transaction.output.values())

        if transaction.input['amount'] != output_total:
            raise Exception("Invalid transaction output values")

        if not Wallet.verify(
                transaction.input['public_key'],
                transaction.output,
                transaction.input['signature']
        ):
            raise Exception("Invalid transaction signature")

    def to_json(self):
        """
        Converts a transaction instance to a json
        :return:
        """
        return self.__dict__

    @staticmethod
    def from_json(transaction_json):
        """
        Deserialise json back into a transaction instance
        :param transaction_json:
        :return:
        """
        return Transaction(**transaction_json)


def main():
    wallet = Wallet()
    transaction = Transaction(wallet, 'recipient', 15)
    print(f'Transaction: {transaction.__dict__}')

    transaction.update(wallet, 'new_recipient', 23)

    print(f'Updated txn: {transaction.__dict__}')

    txn_json = transaction.to_json()
    txn_restored = Transaction.from_json(txn_json)
    print(f'Txn restored from json: {txn_restored.__dict__}')


if __name__ == '__main__':
    main()
