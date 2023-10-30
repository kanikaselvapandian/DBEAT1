from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS, cross_origin
app = Flask(__name__,template_folder="templates/")

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


if __name__ == "__main__":
  app.run()