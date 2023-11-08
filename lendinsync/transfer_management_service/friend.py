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
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/lis_friend'
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/lis_friend'

except KeyError:
	if platform == "darwin":
		app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/lis_friend'
	else:
		app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/lis_friend'

# Disable modification tracking if unnecessary as it requires extra memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

app.logger.setLevel(logging.DEBUG)

db = SQLAlchemy(app)

CORS(app) 

class Friend(db.Model):
    __tablename__ = 'Friend'

    # Define database columns
    fid = db.Column(db.Integer, primary_key=True)
    friend_id = db.Column(db.String(512), nullable=False)  # Match the column name in the table
    friendee_id = db.Column(db.String(512), nullable=False)  # Match the column name in the table
    friendee_name = db.Column(db.String(512), nullable=False)  # Match the column name in the table

    # Initialize class variables
    def __init__(self, friend_id, friendee_id, friendee_name):
        self.friend_id = friend_id
        self.friendee_id = friendee_id
        self.friendee_name = friendee_name

    def json(self):
        return {
            "fid": self.fid,
            "friend_id": self.friend_id,
            "friendee_id": self.friendee_id,
            "friendee_name": self.friendee_name
        }

@app.route("/friends/<string:friend_id>", methods=["GET"])
def get_all_friends(friend_id):
    friend_list = Friend.query.filter_by(friend_id=friend_id).all()
    if friend_list:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "friends": [friend.json() for friend in friend_list]
                }
            }
        )
    else:
        return jsonify(
            {
                "code": 404,
                "message": "There are no friends found."
            }
        ), 404
    
# This route expects 'friend_id' as part of the URL
@app.route("/submit_friend/<string:friend_id>", methods=["POST"])
def createFriend(friend_id):
    # Extract data from the form
    data = request.get_json()
    friendee_id = data.get('friendee_id')
    friendee_name = data.get('friendee_name')

    # Create a new Friend instance
    friend = Friend(
        friend_id=friend_id,
        friendee_id=friendee_id,
        friendee_name=friendee_name
    )

    try:
        # Add the friend to the database session
        db.session.add(friend)
        db.session.commit()  # Commit the changes to the database

        return jsonify({
            "code": 201,
            "data": friend.json(),
            "message": "Friend added successfully to the database"
        }), 201

    except Exception as e:
        db.session.rollback()  # Rollback the transaction in case of an error
        return jsonify({
            "code": 500,
            "message": "An error occurred while adding the friend to the database: " + str(e)
        }), 500

if __name__ == '__main__':
    app.run(port=8895, debug=True)
