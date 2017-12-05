import json
from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
import requests

api_url = 'http://10.5.92.201:5000/'
#api_url = 'http://localhost:5000/'
app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST','GET'])
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/features')
def feature():
    
    return render_template('features.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('login.html')

@app.route('/categorylist')
def categorylist():
    return render_template('categorylist.html')

@app.route('/transactionhistory')
def viewtransactionhistory():
    return render_template('transactionhistory.html')

@app.route('/managerecords')
def managerecords():
    return render_template('manage-records.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)