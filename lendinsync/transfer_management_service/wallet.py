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
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/lis_wallet'
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/lis_wallet'

except KeyError:
	if platform == "darwin":
		app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/lis_wallet'
	else:
		app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/lis_wallet'

# Disable modification tracking if unnecessary as it requires extra memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

app.logger.setLevel(logging.DEBUG)

db = SQLAlchemy(app)

# Create wallet database
class Wallet(db.Model):
    __tablename__ = 'Wallet'

    # Define database columns
    # CHECK VARIABLES
    WID = db.Column(db.Integer, primary_key=True)
    CustomerId = db.Column(db.String(128), nullable=False)
    CurrencyCode = db.Column(db.String(128), nullable=False)
    Amount = db.Column(db.DECIMAL(), nullable=True)

    # Initialize wallet variables
    def __init__(self, CustomerId, CurrencyCode, Amount):
        self.CustomerId = CustomerId
        self.CurrencyCode = CurrencyCode
        self.Amount = Amount

    def json(self):
        return {
                "WID": self.WID, 
                "CustomerId": self.CustomerId, 
                "CurrencyCode": self.CurrencyCode,
                "Amount": self.Amount,
        }

# [GET] Fetch All Wallets
@app.route("/wallet")
def get_all_wallets():
    walletlist = Wallet.query.all()
    if len(walletlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "wallets": [wallet.json() for wallet in walletlist]
                }
            }
        )
        
    return jsonify(
        {
            "code": 404,
            "message": "There are no wallets."
        }
    ), 404

# [GET] Find Wallets Using CustomerId
@app.route("/wallet/<string:CustomerId>")
def find_wallets(CustomerId):
    wallets = Wallet.query.filter_by(CustomerId=CustomerId).all()
    if len(wallets):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "wallet": [wallet.json() for wallet in wallets]
                } 
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No wallets are found."
        }
    ), 404

# [POST] Create Wallet Using CustomerId
@app.route("/wallet", methods=['POST'])
def create_wallet():
    data = request.get_json()
    customer_id = data.get('CustomerId')
    currency_code = data.get('CurrencyCode')
    amount = data.get('Amount')

    # Initialize Wallet without WID since it's auto-generated
    wallet = Wallet(CustomerId=customer_id, CurrencyCode=currency_code, Amount=amount)

    try:
        db.session.add(wallet)
        db.session.commit()
        return jsonify(
                {
                    "code": 201,
                    "data": wallet.json(),
                    "message": "Wallet submitted successfully"
                }
            ), 201
    except Exception as e:
        print(str(e))  # Log the specific error for debugging purposes
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the wallet"
            }
        ), 500


# [PUT] Update Wallet Amount Using WID
@app.route("/wallet/<string:WID>", methods=['PUT'])
def update_wallet_amount(WID):
    wallet = Wallet.query.filter_by(WID=WID).first()

    if wallet:
        data = request.get_json()
        new_amount = data.get('Amount')

        # Update the Amount in the wallet
        wallet.Amount = new_amount

        try:
            db.session.commit()
            return jsonify({
                "code": 200,
                "data": wallet.json(),
                "message": "Wallet amount updated successfully"
            }), 200
        except Exception as e:
            print(str(e))  # Log the specific error for debugging purposes
            return jsonify({
                "code": 500,
                "message": "An error occurred updating the wallet amount"
            }), 500

    return jsonify({
        "code": 404,
        "data": {"WID": WID},
        "message": "Wallet not found."
    }), 404

# [DELETE] Update Wallet Using WID
@app.route("/wallet/<string:WID>", methods=['DELETE'])
def delete_wallet(WID):
    if (Wallet.query.filter_by(WID=WID).first()):

        wallet = Wallet.query.filter_by(WID=WID).first()

        db.session.delete(wallet)
        db.session.commit()

        return jsonify(
            {
                "code": 201,
                "data": wallet.json()
            }
        ), 201

    return jsonify(
        {
            "code": 404,
            "data": {
                "WID": WID
            },
            "message": "Wallet not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(port=7000, debug=True)