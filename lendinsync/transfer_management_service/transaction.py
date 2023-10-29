import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging
from sys import platform
from datetime import datetime
import json
from os import environ

app = Flask(__name__)
# Code assumes Mac or Windows default settings if 'dbURL' does not exist. URI format: dialect+driver://username:password@host:port/database
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('dbURL')
    if app.config['SQLALCHEMY_DATABASE_URI'] == None:
        if platform == "darwin":
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/lis_transaction'
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/lis_transaction'

except KeyError:
	if platform == "darwin":
		app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/lis_transaction'
	else:
		app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/lis_transaction'

# Disable modification tracking if unnecessary as it requires extra memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

app.logger.setLevel(logging.DEBUG)

db = SQLAlchemy(app)

CORS(app) 

# Create wallet database
class Transaction(db.Model):
    __tablename__ = 'WalletTransaction'

    # Define database columns
    TID = db.Column(db.Integer, primary_key=True)
    SourceWallet = db.Column(db.Integer, nullable=True)
    DestinationWallet = db.Column(db.Integer, nullable=True)
    AmountTransferred = db.Column(db.DECIMAL(precision=18, scale=2), nullable=True)
    CustomerId = db.Column(db.String(128), nullable=False)
    WalletTransaction = db.Column(db.Boolean, nullable=False)
    ExchangeRate = db.Column(db.DECIMAL(precision=18, scale=5), nullable=False)
    TimeStamp = db.Column(db.TIMESTAMP, nullable=False)

    # Initialize wallet variables
    def __init__(self, SourceWallet, DestinationWallet, AmountTransferred, CustomerId, WalletTransaction, ExchangeRate, TimeStamp):
        self.SourceWallet = SourceWallet
        self.DestinationWallet = DestinationWallet
        self.AmountTransferred = AmountTransferred
        self.CustomerId = CustomerId
        self.WalletTransaction = WalletTransaction
        self.ExchangeRate = ExchangeRate
        self.TimeStamp = TimeStamp

    def json(self):
        return {
                "TID": self.TID, 
                "SourceWallet": self.SourceWallet,
                "DestinationWallet": self.DestinationWallet,
                "AmountTransferred": self.AmountTransferred,
                "CustomerId": self.CustomerId,
                "WalletTransaction": self.WalletTransaction,
                "ExchangeRate": self.ExchangeRate,
                "TimeStamp": self.TimeStamp
        }

# [GET] Fetch All Transactions
@app.route("/transaction")
def get_all_transactions():
    transaction_list = Transaction.query.all()
    if len(transaction_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "transactions": [transaction.json() for transaction in transaction_list]
                }
            }
        )
        
    return jsonify(
        {
            "code": 404,
            "message": "There are no transactions."
        }
    ), 404

# [GET] Find Transactions Using CustomerId
@app.route("/transaction/<string:CustomerId>")
def find_wallets(CustomerId):
    transaction_list = Transaction.query.filter_by(CustomerId=CustomerId).all()
    if len(transaction_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "transactions": [transaction.json() for transaction in transaction_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No transactions are found."
        }
    ), 404

# [POST] Create Transactions Using TID
@app.route("/transaction", methods=['POST'])
def create_transaction():
    data = request.get_json()

    # Extract the values from the JSON
    source_wallet = data.get('SourceWallet')
    destination_wallet = data.get('DestinationWallet')
    amount_transferred = data.get('AmountTransferred')
    customer_id = data.get('CustomerId')
    wallet_transaction = data.get('WalletTransaction')
    exchange_rate = data.get('ExchangeRate')
    timestamp = data.get('TimeStamp')

    # Create a new Transaction object
    transaction = Transaction(
        SourceWallet=source_wallet,
        DestinationWallet=destination_wallet,
        AmountTransferred=amount_transferred,
        CustomerId=customer_id,
        WalletTransaction=wallet_transaction,
        ExchangeRate=exchange_rate,
        TimeStamp=timestamp
    )

    try:
        db.session.add(transaction)
        db.session.commit()
        return jsonify(
            {
                "code": 201,
                "data": transaction.json(),
                "message": "Transaction completed successfully"
            }
        ), 201
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred completing the transaction"
            }
        ), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)