from flask import Flask, request, jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/loan'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

# [GET] Fetch All Loans
@app.route("/loan")
def get_all_loans():
    loanlist = Loan.query.all()
    if len(loanlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "loans": [loan.json() for loan in loanlist]
                }
            }
        )
        
    return jsonify(
        {
            "code": 404,
            "message": "There are no loans."
        }
    ), 404

# [GET] Find Loans Using CustomerId
@app.route("/loan/<string:CustomerId>")
def find_loans(CustomerId):
    loans = Loan.query.filter_by(CustomerId=CustomerId).all()
    if len(loans):
        return jsonify(
            {
                "code": 200,
                "data": loans.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No loans are found."
        }
    ), 404

# [POST] Create Loan Using CustomerId
@app.route("/loan/<string:LoanId>", methods=['POST'])
def create_loan(LoanId):
    # if (Loan.query.filter_by(LoanId=LoanId).first()):
    #     return jsonify(
    #         {
    #             "code": 400,
    #             "data": {
    #                 "LoanId": LoanId
    #             },
    #             "message": "Loan already exists."
    #         }
    #     ), 400

    data = request.get_json()
    loan = Loan(LoanId, **data)

    try:
        db.session.add(loan)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "LoanId": LoanId
                },
                "message": "An error occurred creating the loan."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": loan.json()
        }
    ), 201

# [GET] Find Loans Using CustomerId based on status
@app.route("/loan/<string:CustomerId>/<string:Status>")
def find_loans_status(CustomerId, Status):
    loans = Loan.query.filter_by(CustomerId=CustomerId, Status=Status).all()
    if len(loans):
        return jsonify(
            {
                "code": 200,
                "data": loans.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No loans are found."
        }
    ), 404

# [PUT] Update Loan Using LoanId
@app.route("/loan/<string:LoanId>", methods=['PUT'])
def update_loan(LoanId):
    loan = Loan.query.filter_by(LoanId=LoanId).first()
    if loan:
        data = request.get_json()
        if data['CollateralAmount']:
            loan.CollateralAmount = data['CollateralAmount']
        if data['LoanAmount']:
            loan.LoanAmount = data['LoanAmount']
        if data['InvestmentAmount']:
            loan.InvestmentAmount = data['InvestmentAmount']
        if data['InterestRate']:
            loan.InterestRate = data['InterestRate']
        if data['CurrencyCode']:
            loan.CurrencyCode = data['CurrencyCode']
        if data['TotalInterestAmount']:
            loan.TotalInterestAmount = data['TotalInterestAmount']
        if data['ServiceFee']:
            loan.ServiceFee = data['ServiceFee']
        if data['RepaymentAmount']:
            loan.RepaymentAmount = data['RepaymentAmount']
        if data['Revenue']:
            loan.Revenue = data['Revenue']
        if data['LoanTerm']:
            loan.LoanTerm = data['LoanTerm']
        if data['StartDate']:
            loan.StartDate = data['StartDate']
        if data['EndDate']:
            loan.EndDate = data['EndDate']
        if data['Status']:
            loan.Status = data['Status']
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": loan.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "LoanId": LoanId
            },
            "message": "Loan not found."
        }
    ), 404

# [DELETE] Update Loan Using LoanId
@app.route("/loan/<string:LoanId>", methods=['DELETE'])
def delete_loan(LoanId):
    loan = Loan.query.filter_by(LoanId=LoanId).first()
    if loan:
        db.session.delete(loan)
        db.session.commit()
        return jsonify(
            {
                "code": 201,
                "data": loan.json()
            }
        ), 201
    return jsonify(
        {
            "code": 404,
            "data": {
                "LoanId": LoanId
            },
            "message": "Loan not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)