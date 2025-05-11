from flask import Flask, request, jsonify, render_template
import json
import time
import uuid
from utils import save_trade_to_s3

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")


@app.route('/trade', methods=['POST'])
def log_trade():
    trade = request.get_json()
    required_fields = {"user_id", "symbol", "qty", "price", "type"}

    if not trade or not required_fields.issubset(trade):
        return jsonify({"error": "Missing required trade fields"}), 400

    trade['timestamp'] = time.time()
    trade['trade_id'] = str(uuid.uuid4())

    try:
        save_trade_to_s3(trade)
        return jsonify({"message": "Trade logged", "trade_id": trade["trade_id"]}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
