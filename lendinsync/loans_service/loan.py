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
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/lis_loan'
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/lis_loan'

except KeyError:
	if platform == "darwin":
		app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/lis_loan'
	else:
		app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/lis_loan'

# Disable modification tracking if unnecessary as it requires extra memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

app.logger.setLevel(logging.DEBUG)

db = SQLAlchemy(app)

CORS(app)

#create loan database
class Loan(db.Model):
    __tablename__ = 'Loan'

    # Define database columns
    # CHECK VARIABLES
    LoanId = db.Column(db.String(128), primary_key=True)
    CustomerId = db.Column(db.String(128), nullable=False)
    CollateralAmount = db.Column(db.String(10), nullable=True)
    LoanAmount = db.Column(db.String(10), nullable=True)
    InvestmentAmount = db.Column(db.String(10), nullable=True)
    InterestRate = db.Column(db.String(128), nullable=False)
    CurrencyCode = db.Column(db.String(128), nullable=False)
    TotalInterestAmount = db.Column(db.String(10), nullable=False)
    ServiceFee = db.Column(db.String(10), nullable=False)
    RepaymentAmount = db.Column(db.String(10), nullable=True)
    Revenue = db.Column(db.String(10), nullable=True)
    LoanTerm = db.Column(db.String(128), nullable=False)
    StartDate = db.Column(db.String(128), nullable=False)
    EndDate = db.Column(db.String(128), nullable=False)
    Status = db.Column(db.String(128), nullable=False)

    # Initialize loan variables
    def __init__(self, LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode, TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, Status):
        self.LoanId = LoanId
        self.CustomerId = CustomerId
        self.CollateralAmount = CollateralAmount
        self.LoanAmount = LoanAmount
        self.InvestmentAmount = InvestmentAmount
        self.InterestRate = InterestRate
        self.CurrencyCode = CurrencyCode
        self.TotalInterestAmount = TotalInterestAmount
        self.ServiceFee = ServiceFee
        self.RepaymentAmount = RepaymentAmount
        self.Revenue = Revenue
        self.LoanTerm = LoanTerm
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.Status = Status

    def json(self):
        return {
                "LoanId": self.LoanId, 
                "CustomerId": self.CustomerId,
                "CollateralAmount": self.CollateralAmount,
                "LoanAmount": self.LoanAmount,
                "InvestmentAmount": self.InvestmentAmount,
                "InterestRate": self.InterestRate,
                "CurrencyCode": self.CurrencyCode,
                "TotalInterestAmount": self.TotalInterestAmount,
                "ServiceFee": self.ServiceFee,
                "RepaymentAmount": self.RepaymentAmount,
                "Revenue": self.Revenue,
                "LoanTerm": self.LoanTerm,
                "StartDate": self.StartDate,
                "EndDate": self.EndDate,
                "Status": self.Status
        }

# [GET] Fetch All borrowing loans
@app.route("/loan/borrowing")
def get_all_borrowing_loans():
    loan_list = Loan.query.filter_by(Status="Borrowing").all()
    if len(loan_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "loans": [loan.json() for loan in loan_list]
                }
            }
        )
        
    return jsonify(
        {
            "code": 404,
            "message": "There are no borrowing loans."
        }
    ), 404

# [GET] Fetch All lending loans
@app.route("/loan/lending")
def get_all_lending_loans():
    loan_list = Loan.query.filter_by(Status="Lending").all()
    if len(loan_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "loans": [loan.json() for loan in loan_list]
                }
            }
        )
        
    return jsonify(
        {
            "code": 404,
            "message": "There are no lending loans."
        }
    ), 404

# [POST] Create borrowing loan based on CustomerId
@app.route("/loan/borrowing/<string:CustomerId>", methods=['POST'])
def create_borrowing_loan(CustomerId):
    data = request.get_json()
    loan = Loan(CustomerId, **data)

    try:
        db.session.add(loan)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the borrowing loan."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": loan.json()
        }
    ), 201

# [POST] Create lending loan based on CustomerId
@app.route("/loan/lending/<string:CustomerId>", methods=['POST'])
def create_lending_loan(CustomerId):
    data = request.get_json()
    loan = Loan(CustomerId, **data)

    try:
        db.session.add(loan)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the lending loan."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": loan.json()
        }
    ), 201

# [GET] Fetch All borrowing loans based on CustomerId
@app.route("/loan/borrowing/<string:CustomerId>")
def get_all_borrowing_loans_by_customer_id(CustomerId):
    loan_list = Loan.query.filter_by(CustomerId=CustomerId, Status="Borrowing").all()
    if len(loan_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "loans": [loan.json() for loan in loan_list]
                }
            }
        )
        
    return jsonify(
        {
            "code": 404,
            "message": "There are no borrowing loans."
        }
    ), 404

# [GET] Fetch All lending loans based on CustomerId
@app.route("/loan/lending/<string:CustomerId>")
def get_all_lending_loans_by_customer_id(CustomerId):
    loan_list = Loan.query.filter_by(CustomerId=CustomerId, Status="Lending").all()
    if len(loan_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "loans": [loan.json() for loan in loan_list]
                }
            }
        )
        
    return jsonify(
        {
            "code": 404,
            "message": "There are no lending loans."
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5001, debug=True)