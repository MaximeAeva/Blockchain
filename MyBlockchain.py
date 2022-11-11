from collections import OrderedDict
import hashlib
import numpy as np
import json
from time import time


class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.new_block(previous_hash=1, nounce=100)
        
    def new_block(self, nounce, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'nounce': nounce,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []

        self.chain.append(block)
        return block
    
    def new_transaction(self, sender_adress, recipient_adress, value):
        self.current_transactions.append({
            'sender_adress': sender_adress,
            'recipient_adress': recipient_adress,
            'value': value
            })
        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    def chain_info(self, ident=None):
        if ident:
            print("Chain : ", self.chain[ident])
            print("Length : ", len(self.chain[ident]))
        else:
            print("Chain : ", self.chain)
            print("Length : ", len(self.chain))
        
    def mine(self, node_ident):
        # Find the next nounce to ine the block
        prev_nounce = self.last_block['nounce']
        nounce = self.proof_of_work(prev_nounce)

        # Get the reward (last block transaction)
        self.new_transaction(0, node_ident, 1)

        # Build the block 
        self.new_block(nounce, self.hash(self.last_block))

        print("New Block Forged")
        print(self.chain_info(-1))

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]
    
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

bc = Blockchain()
bc.chain_info()
bc.new_transaction("a", "b", 50)
bc.new_transaction("c", "d", 10)
bc.mine("Maxime")
bc.chain_info(-1)