from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/wallet'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create wallet database
class Wallet(db.Model):
    __tablename__ = 'Wallet'

    # Define database columns
    # CHECK VARIABLES
    WID = db.Column(db.String(3), primary_key=True)
    CustomerId = db.Column(db.String(128), nullable=False)
    CurrencyCode = db.Column(db.String(128), nullable=False)
    Amount = db.Column(db.String(10), nullable=True)

    # Initialize wallet variables
    def __init__(self, WID, CustomerId, CurrencyCode, Amount):
        self.WID = WID
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
                "data": wallets.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No wallets are found."
        }
    ), 404

# [POST] Create Wallet Using CustomerId
@app.route("/wallet/<string:WID>", methods=['POST'])
def create_wallet(WID):
    # if (Wallet.query.filter_by(WID=WID).first()):
    #     return jsonify(
    #         {
    #             "code": 400,
    #             "data": {
    #                 "WID": WID
    #             },
    #             "message": "Wallet already exists."
    #         }
    #     ), 400

    data = request.get_json()
    # CHECK if first attribute is PK
    wallet = Wallet(WID, **data)

    try:
        db.session.add(wallet)
        db.session.commit()
        
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "WID": WID
                },
                "message": "An error occurred creating the wallet."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": wallet.json()
        }
    ), 201

# [PUT] Update Wallet Using WID
@app.route("/wallet/<string:WID>", methods=['PUT'])
def update_wallet(WID):
    if (Wallet.query.filter_by(WID=WID).first()):

        data = request.get_json()
        print(type(data))
        wallet = Wallet(WID, **data)

        wallet.CustomerId = data['CustomerId']
        wallet.CurrencyCode = data['CurrencyCode']
        wallet.Amount = data['Amount']

        db.session.commit()

        return jsonify(
            {
                "code": 200,
                "data": wallet.json()
            }
        ), 200

    return jsonify(
        {
            "code": 404,
            "data": {
                "WID": WID
            },
            "message": "Wallet not found."
        }
    ), 404

# [DELETE] Update Wallet Using WID
@app.route("/wallet/<string:WID>", methods=['DELETE'])
def delete_walled(WID):
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