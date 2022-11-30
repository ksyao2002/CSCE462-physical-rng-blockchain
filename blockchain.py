import ecdsa
from ecdsa import SigningKey, VerifyingKey,NIST384p
import codecs
import pickle
import json
import time
from hashlib import sha256

#NOTE: Don't change publickey, or else you will isolate yourself from the rest of the protocol

f = open('pk','rb')

sk = SigningKey.from_der(pickle.load(f))
f.close()

f = open('publickey','rb')
vk = VerifyingKey.from_der(pickle.load(f))
f.close()
sig = sk.sign(b"message")
res = vk.verify(sig, b"message") # True

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
    
    def compute_hash(self):
        block_string = str(self.index) + str(json.dumps(self.transactions)) + str(self.timestamp) + str(self.previous_hash)
        return sha256(block_string.encode()).hexdigest()

class Blockchain: 
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()
        self.vk = VerifyingKey.from_der(pickle.load(open('publickey','rb')))
 
    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
    
    def print_chain(self):
        print('length: ',len(self.chain))
        for block in self.chain:
            print('index: ',block.index)
            print('transactions: ',block.transactions)
            print('timestamp: ',block.timestamp)
            print('previous_hash: ',block.previous_hash)
            print('hash: ',block.hash)
            if block.index !=0:
                print('signature: ',block.signature)
            print()

    def validate_chain(self):
        prev = None
        for block in self.chain:
            if prev is None:
                prev = block
                continue
            if prev.hash != block.previous_hash: #make sure the hashes have not been changed
                return False
            if self.vk.verify(block.signature, bytes(block.hash, 'utf-8')):
                return False
        return True

    def add_new_transaction(self, transaction):
                self.unconfirmed_transactions.append(transaction)
    
    def mine(self, pk):
            #if not self.unconfirmed_transactions:
            #    return False
            
            last_block = self.last_block
    
            new_block = Block(index=last_block.index + 1,
                            transactions=self.unconfirmed_transactions,
                            timestamp=time.time(),
                            previous_hash=last_block.hash)
            
            new_block.hash = new_block.compute_hash()
            new_block.signature = pk.sign(bytes(new_block.hash,'utf-8'))
            self.chain.append(new_block)
            
            
            self.unconfirmed_transactions = []
            return new_block.index
    @property
    def last_block(self):
        return self.chain[-1]
