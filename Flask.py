from flask import Flask, jsonify, request
app = Flask(__name__)

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
        return jsonify({"message": "No transactions to mine"}), 400

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
    app.run(host='127.0.0.1', port=5000, debug=False)