from flask import Flask, jsonify, request, make_response, json
from passlib.hash import sha256_crypt
from flask_pymongo import PyMongo
import jwt
import datetime
import base64
import re

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'accounting-system'
app.config['SECRET'] = 'secret'
mongo = PyMongo(app)

# register user
@app.route('/users', methods=['POST'])
def create_user():
    # check if request is json
    if request.is_json:
        data = request.get_json()
        # check for username key if existing
        if "username" not in data:
            error = {"invalid_fields": [{"field": 'username',"reason": "'username' is a required property"}]}
            error_str = json.dumps(error)
            response = make_response(error_str, 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        # check for password key if existing
        elif "password" not in data:
            error = {"invalid_fields": [{"field": 'null',"reason": "'password' is a required property"}]}
            error_str = json.dumps(error)
            response = make_response(error_str, 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            # check password if in pattern, return 400 response error if not match, else continue
            pattern = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\\w\\s]).{8,}$")
            if not pattern.match(data['password']):
                error = {"invalid_fields": [{"field": 'password', "reason": "'string' does not match '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\\\\w\\\\s]).{8,}$'"}]}
                error_str = json.dumps(error)
                response = make_response(error_str, 400)
                response.headers['Content-Type'] = 'application/json'
                return response
        # Insert database section
        # Encrypt password
        hashed_password = sha256_crypt.hash(data['password'])
        data['password'] = hashed_password

        # check for existing user
        users = mongo.db.users
        q = users.find_one({'username':data['username']})
        if q:
            error = {"invalid_fields": [{"field": 'username',
                                         "reason": "User "+data['username']+" already existed"}]}
            error_str = json.dumps(error)
            response = make_response(error_str, 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            if mongo.db.users.insert(data):
                # Return response
                return_data = {"balance": data['balance'],"email": data['email'],"phone": data['phone'],"username": data['username']}
                return_data_str = json.dumps(return_data)
                response = make_response(return_data_str, 200)
                response.headers['Content-Type'] = 'application/json'
                return response
            else:
                error = {'message': "there's something wrong with inserting the data"}
                error_str = json.dumps(error)
                response = make_response(error_str, 400)
                response.headers['Content-Type'] = 'application/json'
                return response
    # return error of not a json request
    else:
        error = {'message': 'content type error'}
        error_str = json.dumps(error)
        response = make_response(error_str, 400)
        response.headers['Content-Type'] = 'application/json'
        return response

# user login
@app.route('/users/login', methods=['POST'])
def login_user():
    basic_auth = request.headers.get("Authorization")
    basic_auth = basic_auth.replace("Basic","")
    basic_auth = base64.b64decode(basic_auth)
    basic_auth = basic_auth.decode('utf-8')

    if ':' not in basic_auth:
        error = {'message': "Invalid username or password"}
        error_str = json.dumps(error)
        response = make_response(error_str, 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    users = mongo.db.users
    username = basic_auth.split(':')[0]
    password = basic_auth.split(':')[1]
    q = users.find_one({'username':username})
    if q:
        if sha256_crypt.verify(password,q['password']):
            # make token
            try:
                payload = {
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=10),
                        'iat': datetime.datetime.utcnow(),
                        'sub': q['username']
                    }
                return jwt.encode(
                        payload,
                        app.config['SECRET'],
                        algorithm='HS256'
                    )

            except Exception as e:
                return e
    error = {'message': "Invalid username or password"}
    error_str = json.dumps(error)
    response = make_response(error_str, 401)
    response.headers['Content-Type'] = 'application/json'
    return response

# user logout
@app.route('/users/logout')
def logout():
    token_key = request.headers.get('Authorization')
    jwt.decode()
    # blacklisted = mongo.db.blacklisted
    # blacklisted.insert({'username':})


@app.route('/users/<username>',methods=['GET'])
def get_users():
    pass

if __name__ == '__main__':
    app.run()


