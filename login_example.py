from flask import Flask, render_template, url_for, request, session, redirect
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
import os

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "mpark-try-flask-login"
app.config["MONGO_URI"] = "mongodb://root:Madeforroot1@ds147180.mlab.com:47180/mpark-try-flask-login"

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']
    return render_template('index.html')
    
@app.route("/login", methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})
    
    if login_user:
        if bcrypt.check_password_hash(login_user['password'], request.form['pass']):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return 'Invalid username/password combination'
    
    return 'Invalid Username'
    
@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name':request.form['username']})
        
        if existing_user is None:
            pw_hash = bcrypt.generate_password_hash(request.form['pass'])
            users.insert({'name' : request.form['username'], 'password' : pw_hash})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
            
        return 'That username already exists!'
    
    return render_template('register.html')


if __name__ == '__main__':
    app.secret_key = 'topsecret'
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)