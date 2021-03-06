# Module 1 - Create a Blockchain

# To be installed:
# Flask == 0.12.2
# Go to $Home
# anaconda3/python -m pip install flask
# Postman HTTP Client

# Import dependencies
import datetime
import hashlib
import json
from flask import Flask, jsonify


# Part 1 - Building a Blockchain


class  Blockchain:
    """ Blochain class """
    def __init__(self):
        """ Constructor """
        self.chain = [] # chain
        self.create_block(proof = 1, previous_hash=0) # genesis block


    def create_block(self, proof, previous_hash):
        """ Create block method """
        block = {'index' : len(self.chain)+1,
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash' : previous_hash
                 }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        """ Get previous block method """
        return self.chain[-1] # last index
    
    def proof_of_work(self, previous_proof):
        """ 'Mine' """
        new_proof = 1 # initialize new proof variable
        check_proof = False
        
        # proof of work problem
        while not(check_proof):
            # hash of non-symmetrical operation (the more complex the better)
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            
            # check for 4 leading zeros
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        
        # return proof of work
        return new_proof
    
    
    def hash(self, block):
        """ Hash block """
        # encode block to string
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
        
    
    def is_chain_valid(self):
        """ Check if chain is valid """
        chain = self.chain
        previous_block = chain[0]
        block_index = 1
        
        # iterate through chain
        while block_index < len(chain):
            block = chain[block_index] # start from index=1
            
            # check consistency of chain
            if block['previous_hash'] != self.hash(previous_block):
                return False # chain is not valid
            
            # check hash
            hash_operation = hashlib.sha256(str(block['proof']**2 - previous_block['proof']**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False # chain is not valid
            
            # increment index
            previous_block = block
            block_index +=1
        
        # chain is valid
        return True

# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)

#Creating a Blockchain
blockchain = Blockchain()

# Start mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof) # mine
    previous_hash = blockchain.hash(previous_block) # hash of block inclufing pow
    block = blockchain.create_block(proof, previous_hash) # append new block to chain
    
    # json response
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block ['timestamp'],
                'proof' : block ['proof'],
                'previous_hash' : block['previous_hash']
        }
    
    # return response, status
    return jsonify(response), 200


# Getting the full Blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length' : len(blockchain.chain)
                }
    
    # return response, status
    return jsonify(response), 200




@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid()
    if is_valid: 
        response = {'message' : 'Chain is valid'}
    else:
    
        response = {'message' :' Chain is NOT valid'}
        
    return jsonify(response), 200



# Running the app
app.run(host='0.0.0.0', port='5000')