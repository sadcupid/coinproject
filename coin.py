from flask import Flask, jsonify, request
import hashlib
import datetime
import random

app = Flask(__name__)

WALLET_ADDRESS = "YourWalletAddressHere"

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
class Block:
    def __init__(self, index, timestamp, transaction, previous_hash, data, nonce =0):
        self.index = index
        self.timestamp = timestamp
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.data =data 
        self.nonce = nonce
        self.hash = self.caculate_hash()

    def caculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.transaction).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.nonce).encode('tuf-8'))
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain =[self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transaction = []
        self.stakeholders = 0
        self.total_coins = 0
        self.max_coins = 50000000

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), [], "0", "Genesis Block")
    
    def get_lastest_block(self):
        return self.chain[-1]
    
    def add_transaction(self, transaction):
        if self.total_coins + transaction > self.max_coins:
            return False
        if transaction.receiver in self.stakeholders:
            receiver_balance = self.stakeholders[transaction.receiver]
            if receiver_balance + transaction.amount > 20000:
                return False
            
        self.pending_transaction.append(transaction)
        return True
    
    def mine_pending_transction(self, miner_address):
        if not self.pending_transaction:
            return
        
        total_stake = sum(self.stakeholders.value())
        random.seed(datetime.datetime.now())
        rand_num = random.uniform(0, total_stake)
        stake_sum = 0
        for address,stake in self.stakeholders.item():
            stake_sum += stake
            if total_stake >= rand_num:
                miner_address = address
                break

        new_block = Block(len(self.chain), datetime.datetime.now(), self.pending_transaction, self.get_lastest_block().hash)
        new_block.nonce = random.randint(0, 1000000)
        new_block.hash = new_block.caculate_hash()
        self.chain.append(new_block)
        self.pending_transaction = []

        block_reward = 100
        self.total_coins += block_reward
        for transaction in new_block.transaction:
            self.total_coins += transaction.amount
            if transaction.receiver in self.stakeholders:
                self.stakeholders[transaction.receiver] += transaction.amount
            else:
                self.stakeholders[transaction.receiver] = transaction.amount

        return True

        print("Block mined successfully by: ", miner_address)

    def add_stakeholder(self, address, stake):
        self.stakeholders[address] = stake

    def update_stake(self, address, new_stakes):
        if address in self.stakeholders:
            self.stakeholders[address] = new_stakes
            print("Stake update successfully for: ", address)
        else:
            print("Stakeholder not found.")
    
    def get_block_by_index(self, index):
        if 0 <= index < len(self.chain):
            return self.chain[index]
        else:
            return None
    def get_blocks_by_data(self,data):
        blocks_with_data = []
        for block in self.chain:
            if block.data == data:
                blocks_with_data(block)
        return blocks_with_data

Maximus_coin = Blockchain()

Maximus_coin.add_stakeholder("TU PHAN", 1000000)

Maximus_coin.add_transaction(Transaction("Sender1","Reciever1"), 5000)
Maximus_coin.add_transaction(Transaction("Sender2","Receiver2"), 10000)
Maximus_coin.add_transaction(Transaction("Sender3","Receiver3"), 15000)
Maximus_coin.add_transaction(Transaction("Sender4","Reciever4"), 20000)

@app.route('/buy_coins', methods=['POST'])
def buy_coins():
    data = request.json
    receiver = data['receiver']
    amount = data['amount']

    transaction = Transaction("Robinhood", receiver, amount)
    if Maximus_coin.add_transaction(transaction):
        return jsonify({"message": "Coins bought successfully"}), 200
    else:
        return jsonify({"message": "Transaction rejected: Limit exceeded"}), 400

@app.route('/mine_coins', methods=['POST'])
def mine_coins():
    if Maximus_coin.mine_pending_transactions("Miner"):
        return jsonify({"message": "Coins mined successfully"}), 200
    else:
        return jsonify({"message": "No transactions"}), 400

@app.route('/get_block/<int:index>', methods=['GET'])
def get_block(index):
    block = Maximus_coin.get_block_by_index(index)
    if block:
        block_data = {
            "index": block.index,
            "timestamp": str(block.timestamp),
            "transactions": [vars(tx) for tx in block.transactions],
            "previous_hash": block.previous_hash,
            "data": block.data,
            "hash": block.hash
        }
        return jsonify(block_data), 200
    else:
        return jsonify({"message": "Block not found"}), 404

if __name__ == '__main__':
    app.run(host='192.268.1.100', port=5000, debug=True)

