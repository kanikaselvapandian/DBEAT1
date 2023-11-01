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
    InterestRate = db.Column(db.String(128), nullable=True)
    CurrencyCode = db.Column(db.String(128), nullable=False)
    TotalInterestAmount = db.Column(db.String(10), nullable=True)
    ServiceFee = db.Column(db.String(10), nullable=False)
    RepaymentAmount = db.Column(db.String(10), nullable=True)
    Revenue = db.Column(db.String(10), nullable=True)
    LoanTerm = db.Column(db.String(128), nullable=False)
    StartDate = db.Column(db.String(128), nullable=True)
    EndDate = db.Column(db.String(128), nullable=True)
    StatusLevel = db.Column(db.String(128), nullable=False)

    # Initialize loan variables
    def __init__(self, LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode, TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel):
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
        self.StatusLevel = StatusLevel

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
                "StatusLevel": self.StatusLevel
        }
    

# [GET] Fetch All borrowing loans
@app.route("/loan/borrowing")
def get_all_borrowing_loans():
    loan_list = Loan.query.filter_by(StatusLevel="Borrowing").all()
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
    loan_list = Loan.query.filter_by(StatusLevel="Lending").all()
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
    
    # Extract the values from the JSON
    customer_id = data.get('CustomerId')
    collateral_amount = data.get('CollateralAmount')
    loan_amount = data.get('LoanAmount')
    currency_code = data.get('CurrencyCode')
    loan_term = data.get('LoanTerm')
    service_fee = data.get('ServiceFee')

    # Create a new Loan object
    loan = Loan(
        CustomerId=CustomerId,
        CollateralAmount=collateral_amount,
        LoanAmount=loan_amount,
        InvestmentAmount=None,
        InterestRate=None,
        CurrencyCode=currency_code,
        TotalInterestAmount=None,
        ServiceFee=service_fee,
        RepaymentAmount=None,
        Revenue=None,
        LoanTerm=loan_term,
        StartDate=None,
        EndDate=None,
        StatusLevel="Borrowing"
    )

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
            "data": loan.json(),  # Add a comma here
            "message": "Borrowing loan created successfully."
        }
    ), 201

# [POST] Create lending loan based on CustomerId
@app.route("/loan/lending/<string:CustomerId>", methods=['POST'])
def create_lending_loan(CustomerId):
    data = request.get_json()
    
    # Extract the values from the JSON
    customer_id = data.get('CustomerId')
    investment_amount = data.get('InvestmentAmount')
    interest_rate = data.get('InterestRate')
    currency_code = data.get('CurrencyCode')
    loan_term = data.get('LoanTerm')
    service_fee = data.get('ServiceFee')
    total_interest_amount = data.get('TotalInterestAmount')
    revenue = data.get('Revenue')
    status_level = "Lending"

    # Create a new Loan object
    loan = Loan(
        CustomerId=CustomerId,
        CollateralAmount=None,
        LoanAmount=None,
        InvestmentAmount=investment_amount,
        InterestRate=interest_rate,
        CurrencyCode=currency_code,
        TotalInterestAmount=total_interest_amount,
        ServiceFee=service_fee,
        RepaymentAmount=None,
        Revenue=revenue,
        LoanTerm=loan_term,
        StartDate=None,
        EndDate=None,
        StatusLevel=status_level
    )

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
            "data": loan.json(),
            "message": "Lending loan created successfully."
        }
    ), 201


# [GET] Fetch All borrowing loans based on CustomerId
@app.route("/loan/borrowing/<string:CustomerId>")
def get_all_borrowing_loans_by_customer_id(CustomerId):
    loan_list = Loan.query.filter(Loan.CustomerId == CustomerId, Loan.StatusLevel.in_(["Borrowing", "BMatch"])).all()
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
    loan_list = Loan.query.filter(Loan.CustomerId == CustomerId, Loan.StatusLevel.in_(["Lending", "LMatch"])).all()
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