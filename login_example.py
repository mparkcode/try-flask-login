from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
import os

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "mpark-try-flask-login"
app.config["MONGO_URI"] = "mongodb://root:Madeforroot1@ds147180.mlab.com:47180/mpark-try-flask-login"

mongo = PyMongo(app)

@app.route("/")
def get_index():
    return render_template("index.html")


if __name__ == '__main__':
    app.secret_key = 'topsecret'
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)