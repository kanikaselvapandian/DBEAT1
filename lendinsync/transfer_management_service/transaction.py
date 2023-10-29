from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
# Code assumes Mac or Windows default settings if 'dbURL' does not exist. URI format: dialect+driver://username:password@host:port/database
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('dbURL')
    if app.config['SQLALCHEMY_DATABASE_URI'] == None:
        if platform == "darwin":
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/fap_application'
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/fap_application'

except KeyError:
	if platform == "darwin":
		app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/fap_application'
	else:
		app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/fap_application'

# Disable modification tracking if unnecessary as it requires extra memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

app.logger.setLevel(logging.DEBUG)

db = SQLAlchemy(app)

CORS(app) 

# Create wallet database
class Transaction(db.Model):
    __tablename__ = 'Transaction'

    # Define database columns
    # CHECK VARIABLES
    TID = db.Column(db.String(3), primary_key=True)
    SourceWallet = db.Column(db.String(128), nullable=True)
    DestinationWallet = db.Column(db.String(128), nullable=True)
    AmountTransferred = db.Column(db.String(10), nullable=True)
    CustomerId = db.Column(db.String(128), nullable=False)
    WalletTransaction = db.Column(db.String(128), nullable=False) #BOOLEAN
    ExchangeRate = db.Column(db.String(128), nullable=False)
    TimeStamp = db.Column(db.String(128), nullable=False)

    # Initialize wallet variables
    def __init__(self, TID, SourceWallet, DestinationWallet, AmountTransferred, CustomerId, WalletTransaction, ExchangeRate, TimeStamp):
        self.TID = TID
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
    transactions = Transaction.query.filter_by(CustomerId=CustomerId).all()
    if len(transactions):
        return jsonify(
            {
                "code": 200,
                "data": transactions.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No transactions are found."
        }
    ), 404

# [POST] Create Transactions Using TID
@app.route("/transaction/<string:TID>", methods=['POST'])
def create_transaction(TID):
    data = request.get_json()

    transaction = Transaction(TID, **data)

    try:
        db.session.add(transaction)
        db.session.commit()
        
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "TID": TID
                },
                "message": "An error occurred completing the transaction."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": transaction.json()
        }
    ), 201

if __name__ == '__main__':
    app.run(port=8000, debug=True)