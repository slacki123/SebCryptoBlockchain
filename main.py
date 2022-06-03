from backend.blockchain.blockchain import Blockchain

if __name__ == '__main__':
    foo_blockchain = Blockchain()
    foo_blockchain.add_block('one')
    foo_blockchain.add_block('two')
    foo_blockchain.add_block('three')
    foo_blockchain.add_block('four')
    foo_blockchain.add_block('five')
    foo_blockchain.add_block('six')


    print(foo_blockchain)
