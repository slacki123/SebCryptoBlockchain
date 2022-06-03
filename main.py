from blockchain import Blockchain

if __name__ == '__main__':
    foo_blockchain = Blockchain()
    foo_blockchain.add_block('one')
    foo_blockchain.add_block('two')
    foo_blockchain.add_block('three')

    print(foo_blockchain)
