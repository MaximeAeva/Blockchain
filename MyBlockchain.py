from collections import OrderedDict
import hashlib
import numpy as np
import json
import random
import string
from time import time

print('\033[0;31;43m CHEESY \033[0;0m')

def PrintStylishChain(chain):
    for block in chain:
        print("\033[0;37;44m", "Block n°", block['index'], "\033[0;0m")
        print("\033[0;33;40m", "\tTimestamp : ", block['timestamp'], "\033[0;0m")
        print("\033[0;33;40m", "\tTransactions (", len(block['transactions']),") : \033[0;0m")
        for transaction in block['transactions']:
            print("\033[0;30;41m\t\t", transaction['sender_adress'],
                 "\033[0;0m -> \033[0;0;42m",
                  transaction['recipient_adress'], "\033[0;0m ", transaction['value'])
        print("\033[0;33;40m", "\tNounce : ", block['nounce'], "\033[0;0m")
        print("\033[0;33;40m", "\tPrevious_Hash : ", block['previous_hash'], "\033[0;0m")

class Node(object):
    def __init__(self):
        result = []
        for i in range(32):
            result.append(str(random.choice("0123456789abcdef")))
        self.adress = "".join(result)
        self.content = 0
    
    def get_content(self):
        return self.content

    def update_content(self, chain):
        for block in chain:
            for transaction in block["transactions"]:
                if transaction["recipient_adress"] == self.adress:
                    self.content += transaction["value"]
                if transaction["sender_adress"] == self.adress:
                    self.content -= transaction["value"]

    def get_adress(self):
        return self.adress

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.new_block(previous_hash=1, nounce=100)

        self.nodes = set()
        
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
            print("Block : ", self.chain[ident])
            print("Block length : ", len(self.chain[ident]["transactions"]))
        else:
            print("Chain : ", self.chain)
            print("Chain length : ", len(self.chain))
        
    def mine(self, node_ident):
        # Find the next nounce to ine the block
        prev_nounce = self.last_block['nounce']
        nounce = self.proof_of_work(prev_nounce)

        Reward = 0
        for transaction in self.current_transactions:
            Reward += transaction['value']

        # Get the reward (last block transaction)
        self.new_transaction("Reward                          ", node_ident, 0.1*Reward)

        # Build the block 
        self.new_block(nounce, self.hash(self.last_block))

        print("New Block Forged")
        print(self.chain_info(-1))

    def register_node(self, node):
        self.nodes.add(node)

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index<len(chain):
            block = chain[current_index]

            if block['previous_hash'] != self.hash(last_block):
                return False
            
            if not self.valid_proof(last_block['nounce'], block['nounce']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflict(self):
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:
            chain = node.get_chain()
            if len(chain) > max_length and self.valid_chain(chain):
                max_length = len(chain)
                naw_chain = chain
            
        if new_chain:
            self.chain = new_chain
            return True
        
        return False

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



print("Initialize Blockchain")
bc = Blockchain()

print("First Block")
bc.chain_info()

# Nodes for mining and training 
a = Node()
b = Node()
c = Node()

# Registering nodes
bc.register_node(a)
bc.register_node(b)
bc.register_node(c)

# Giving an account
bc.new_transaction("Network                         ", a.get_adress(), random.randint(0, 100))
bc.new_transaction("Network                         ", b.get_adress(), random.randint(0, 100))
bc.new_transaction("Network                         ", c.get_adress(), random.randint(0, 100))
a.update_content(bc.chain)
b.update_content(bc.chain)
c.update_content(bc.chain)
print("a : ", a.get_content())
print("b : ", b.get_content())
print("c : ", c.get_content())

# Transaction
bc.new_transaction(a.get_adress(), b.get_adress(), 50)
bc.new_transaction(a.get_adress(), c.get_adress(), 30)
bc.new_transaction(c.get_adress(), b.get_adress(), 60)

# Mining and adding new block
bc.mine(a.get_adress())

a.update_content(bc.chain)
b.update_content(bc.chain)
c.update_content(bc.chain)
print("a : ", a.get_content())
print("b : ", b.get_content())
print("c : ", c.get_content())

PrintStylishChain(bc.chain)
