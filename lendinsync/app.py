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
      
@app.route("/home")
def homePage():
    try:
         return render_template("home.html")
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route("/ui")
def homeUI():
    try:
         return render_template("hometest.html")
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
  app.run(debug=True)