import json
from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
import requests

api_url = 'http://localhost:5000/'

app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST','GET'])
def register():

    if request.method == 'POST':
        url = api_url+"users"

        payload = "{\r\n  \"username\": \"kyle_halog\",\r\n  \"firstName\": \"Albert\",\r\n  \"lastName\": \"Einstein\",\r\n  \"email\": \"albert_einstein@mail.com\",\r\n  \"balance\": 5.99,\r\n  \"phone\": \"021234567\",\r\n  \"password\": \"N0virus?1019\"\r\n}"
        headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "b594c2a5-e179-cf54-5f7d-aebfdb28445e"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('/dashboard.html')

if __name__ == '__main__':
    app.run(port=8080)