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
    LoanId = db.Column(db.Integer, primary_key=True)
    CustomerId = db.Column(db.String(128), nullable=False)
    OtherPartyId = db.Column(db.String(128), nullable=True)
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
    def __init__(self, CustomerId, OtherPartyId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode, TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel):
        self.CustomerId = CustomerId
        self.OtherPartyId = OtherPartyId
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
                "OtherPartyId": self.OtherPartyId,
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
@app.route("/loan/borrowing/", methods=['POST'])
def create_borrowing_loan():
    data = request.get_json()
    CustomerId = data.get('CustomerId')
    collateral_amount = data.get('CollateralAmount')
    loan_amount = data.get('LoanAmount')
    investment_amount = data.get('InvestmentAmount')
    currency_code = data.get('CurrencyCode')
    loan_term = data.get('LoanTerm')
    service_fee = data.get('ServiceFee')

    # Create a new Loan object
    loan = Loan(
        CustomerId=CustomerId,
        OtherPartyId=None,
        CollateralAmount=collateral_amount,
        LoanAmount=loan_amount,
        InvestmentAmount=investment_amount,
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

        return jsonify(
            {
                "code": 201,
                "data": loan.json(), 
                "message": "Borrowing loan created successfully."
            }
        ), 201

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the borrowing loan. " + str(e)
            }
        ), 500

# [POST] Create lending loan based on CustomerId
@app.route("/loan/lending/", methods=['POST'])
def create_lending_loan():
    data = request.get_json()  
    CustomerId = data.get('CustomerId')
    investment_amount = data.get('InvestmentAmount')
    loan_amount = data.get('LoanAmount')
    interest_rate = data.get('InterestRate')
    currency_code = data.get('CurrencyCode')
    loan_term = data.get('LoanTerm')
    repayment_amount = data.get('Revenue')
    service_fee = data.get('ServiceFee')
    total_interest_amount = data.get('TotalInterestAmount')
    revenue = data.get('Revenue')

    # Create a new Loan object
    loan = Loan(
        CustomerId=CustomerId,
        OtherPartyId=None,
        CollateralAmount=None,
        LoanAmount=loan_amount,
        InvestmentAmount=investment_amount,
        InterestRate=interest_rate,
        CurrencyCode=currency_code,
        TotalInterestAmount=total_interest_amount,
        ServiceFee=service_fee,
        RepaymentAmount=repayment_amount,
        Revenue=revenue,
        LoanTerm=loan_term,
        StartDate=None,
        EndDate=None,
        StatusLevel="Lending"
    )

    try:
        db.session.add(loan)
        db.session.commit()

        return jsonify(
            {
                "code": 201,
                "data": loan.json(),
                "message": "Lending loan created successfully."
            }
        ), 201

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the lending loan. " + str(e)
            }
        ), 500


# [GET] Fetch All borrowing loans based on CustomerId
@app.route("/loan/borrowing/<string:CustomerId>")
def get_all_borrowing_loans_by_customer_id(CustomerId):
    loan_list = Loan.query.filter(Loan.CustomerId == CustomerId, Loan.StatusLevel.in_(["Borrowing"])).all()
    lmatch_loans = Loan.query.filter(Loan.OtherPartyId == CustomerId, Loan.StatusLevel == "LMatch").all()
    if len(loan_list) or len(lmatch_loans):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "loans": [loan.json() for loan in loan_list] + [loan.json() for loan in lmatch_loans]
                }
            }
        )
        
    return jsonify(
        {
            "code": 404,
            "message": "There are no borrowing loans or BMatch loans for the given CustomerId."
        }
    ), 404


# [GET] Fetch All lending loans based on CustomerId
@app.route("/loan/lending/<string:CustomerId>")
def get_all_lending_loans_by_customer_id(CustomerId):
    loan_list = Loan.query.filter(Loan.CustomerId == CustomerId, Loan.StatusLevel.in_(["Lending"])).all()
    bmatch_loans = Loan.query.filter(Loan.OtherPartyId == CustomerId, Loan.StatusLevel == "BMatch").all()
    if len(loan_list) or len(bmatch_loans):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "loans": [loan.json() for loan in loan_list] + [loan.json() for loan in bmatch_loans]
                }
            }
        )
        
    return jsonify(
        {
            "code": 404,
            "message": "There are no lending loans or LMatch loans for the given CustomerId."
        }
    ), 404


@app.route("/loan/update/<int:LoanId>", methods=['PUT'])
def update_loan(LoanId):
    data = request.get_json()
    new_interest_rate = data.get('InterestRate')
    new_repayment_amount = data.get('RepaymentAmount')
    new_revenue = data.get('RepaymentAmount')
    new_other_party_id = data.get('OtherPartyId')  # Add this line
    new_StartDate = data.get('StartDate')
    new_EndDate = data.get('EndDate')
    new_TotalInterestAmount = data.get('TotalInterestAmount')
    new_StatusLevel = data.get('StatusLevel')


    try:
        loan = Loan.query.filter_by(LoanId=LoanId).first()
        if not loan:
            return jsonify(
                {
                    "code": 404,
                    "message": "Loan not found."
                }
            ), 404

        if new_interest_rate is not None:
            loan.InterestRate = new_interest_rate
        if new_repayment_amount is not None:
            loan.RepaymentAmount = new_repayment_amount
        if new_revenue is not None:
            loan.Revenue = new_revenue
        if new_other_party_id is not None:  # Add this block
            loan.OtherPartyId = new_other_party_id
        if new_StartDate is not None:
            loan.StartDate = new_StartDate
        if new_EndDate is not None:
            loan.EndDate = new_EndDate
        if new_TotalInterestAmount is not None:
            loan.TotalInterestAmount = new_TotalInterestAmount
        if new_StatusLevel is not None:
            loan.StatusLevel = new_StatusLevel
        

        db.session.commit()

        return jsonify(
            {
                "code": 200,
                "data": loan.json(),
                "message": "Loan updated successfully."
            }
        ), 200

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating the loan. " + str(e)
            }
        ), 500


if __name__ == '__main__':
    app.debug = True
    app.run(port=5001)
