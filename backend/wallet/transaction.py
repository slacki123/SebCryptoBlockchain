import time
import uuid

from backend.wallet.wallet import Wallet


class Transaction:
    """
    Document of an exchange of currency, from a sender to one or more recipients
    """

    def __init__(self, sender_wallet: Wallet, recipient, amount):
        self.id = str(uuid.uuid4())[0:8]
        self.output = self.create_output(
            sender_wallet,
            recipient,
            amount
        )
        self.input = self.create_input(sender_wallet, self.output)

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


def main():
    wallet = Wallet()
    transaction = Transaction(wallet, 'recipient', 15)
    print(f'Transaction: {transaction.__dict__}')

    transaction.update(wallet, 'new_recipient', 23)

    print(f'Updated txn: {transaction.__dict__}')


if __name__ == '__main__':
    main()
