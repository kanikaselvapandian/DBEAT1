from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS, cross_origin
app = Flask(__name__,template_folder="templates/", static_url_path='/DBEAT1/lendinsync/assets', static_folder="assets")

CORS(app)

@app.route("/")
@cross_origin()
def hello():
  return render_template("login.html")

@app.route("/requestOTP")
def requestOTP():
    try:
         return render_template("requestOTP.html")# your code here
    except Exception as e:
        return jsonify({'error': str(e)})
    

@app.route("/profile")
def profile():
    try:
         return render_template("profile.html")# your code here
    except Exception as e:
        return jsonify({'error': str(e)})
      
@app.route("/wallet")
def homePage():
    try:
         return render_template("wallet.html")
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route("/home")
def homeUI():
    try:
         return render_template("home.html")
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route("/marketplace")
def marketplace():
    try:
         return render_template("marketplace.html")
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route("/my_loans")
def my_loans():
    try:
         return render_template("my_loans.html")
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route("/loan/borrowing/")
def create_borrow_application():
    try:
         return render_template("create_borrow_application.html")
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route("/loan/lending/")
def create_lending_application():
    try:
         return render_template("create_lending_application.html")
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
  app.run()