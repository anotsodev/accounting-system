from flask import Flask, request, make_response, json
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

# CATEGORY SECTION
@app.route('/categories',methods=['GET','POST'])
def categories():
    # Start Token Checking
    token_key = request.headers.get('Authorization')
    try:
        decoded = jwt.decode(token_key, app.config['SECRET'], algorithms=['HS256'])
    except:
        error = {'message': "Signature expired. Please log in again."}
        error_str = json.dumps(error)
        response = make_response(error_str, 400)
        response.headers['Content-Type'] = 'application/json'
        return response

    blacklisted = mongo.db.blacklisted
    q = blacklisted.find_one({'username': decoded['sub'], 'token': token_key})
    if q:
        error = {'message': "Authentication information is missing or invalid"}
        error_str = json.dumps(error)
        response = make_response(error_str, 400)
        response.headers['Content-Type'] = 'application/json'
        return response
    # End of Token Checking

    # Check request method if POST to insert data to db
    if request.method == 'POST':
        if request.is_json:
            types = ['income','expense']
            data = request.get_json()
            # Check body if valid
            if "name" not in data:
                error = {'message': 'invalid request body'}
                error_str = json.dumps(error)
                response = make_response(error_str, 400)
                response.headers['Content-Type'] = 'application/json'
                return response
            if "type" not in data:
                error = {'message': 'invalid request body'}
                error_str = json.dumps(error)
                response = make_response(error_str, 400)
                response.headers['Content-Type'] = 'application/json'
                return response
            if data['type'] not in types:
                error = {"invalid_fields": [{"field": "type","reason": data['type']+" is not one of "+str(types)}]}
                error_str = json.dumps(error)
                response = make_response(error_str,400)
                response.headers['Content-Type'] = 'application/json'
                return response
            else:
            # if body is valid, insert data to db
                categories = mongo.db.categories
                q = categories.insert(data)
                if q:
                    categories.update({'_id': q}, {'id': str(q), 'name': data['name'], 'type': data['type']})
                    return_data = {"id":str(q),"name":data['name'],"type":data['type']}
                    return_data_str = json.dumps(return_data)
                    response = make_response(return_data_str,200)
                    response.headers['Content-Type'] = 'application/json'
                    return response
        else:
        # if request content-type is not json, this will return an error response
            error = {'message': 'content type error'}
            error_str = json.dumps(error)
            response = make_response(error_str, 400)
            response.headers['Content-Type'] = 'application/json'
            return response

    # this will return all the categories if the method is not POST
    # by default the method is GET
    categories = mongo.db.categories
    q = categories.find()
    data = []
    for item in q:
        data.append({'id':str(item['_id']),'name':item['name'], 'type':item['type']})

    request_data = json.dumps(data)
    response = make_response(request_data,200)
    response.headers['Content-Type'] = 'application/json'
    return request_data


@app.route('/categories/<category_id>',methods=['GET'])
def view_category(category_id):
    # Start Token Checking
    token_key = request.headers.get('Authorization')
    try:
        decoded = jwt.decode(token_key, app.config['SECRET'], algorithms=['HS256'])
    except:
        error = {'message': "Signature expired. Please log in again."}
        error_str = json.dumps(error)
        response = make_response(error_str, 400)
        response.headers['Content-Type'] = 'application/json'
        return response

    blacklisted = mongo.db.blacklisted
    q = blacklisted.find_one({'username': decoded['sub'], 'token': token_key})
    if q:
        error = {'message': "Authentication information is missing or invalid"}
        error_str = json.dumps(error)
        response = make_response(error_str, 400)
        response.headers['Content-Type'] = 'application/json'
        return response
    # End of Token Checking
    # This will check the category if the category id is same with the request category id
    # this will simply search categories collection with the given category id
    categories = mongo.db.categories
    q = categories.find_one({'id':category_id})
    if q:
        request_data = {'id':q['id'],'name':q['name'],'type':q['type']}
        request_data_str = json.dumps(request_data)
        response = make_response(request_data_str,200)
        response.headers['Content-Type'] = 'application/json'

        return response
    error = {'message': 'category not found'}
    error_str = json.dumps(error)
    response = make_response(error_str, 404)
    response.headers['Content-Type'] = 'application/json'
    return response

# RECORDS SECTION
@app.route('/records',methods=['GET','POST'])
def records():
    # Start Token Checking
    token_key = request.headers.get('Authorization')
    try:
        decoded = jwt.decode(token_key, app.config['SECRET'], algorithms=['HS256'])
    except:
        error = {'message': "Signature expired. Please log in again."}
        error_str = json.dumps(error)
        response = make_response(error_str, 400)
        response.headers['Content-Type'] = 'application/json'
        return response

    blacklisted = mongo.db.blacklisted
    q = blacklisted.find_one({'username': decoded['sub'], 'token': token_key})
    if q:
        error = {'message': "Authentication information is missing or invalid"}
        error_str = json.dumps(error)
        response = make_response(error_str, 400)
        response.headers['Content-Type'] = 'application/json'
        return response
    # end of token checking section
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            if "amount" not in data:
                error = {'message': 'invalid request body'}
                error_str = json.dumps(error)
                response = make_response(error_str, 400)
                response.headers['Content-Type'] = 'application/json'
                return response
            if "category_id" not in data:
                error = {'message': 'invalid request body'}
                error_str = json.dumps(error)
                response = make_response(error_str, 400)
                response.headers['Content-Type'] = 'application/json'
                return response
            if "description" not in data:
                error = {'message': 'invalid request body'}
                error_str = json.dumps(error)
                response = make_response(error_str, 400)
                response.headers['Content-Type'] = 'application/json'
                return response
            else:
                records = mongo.db.records
                q = records.insert(data)
                if q:
                    records.update({'_id': q}, {'id': str(q), 'amount': data['amount'], 'category_id': data['category_id'],'description':data['description']})
                    return_data = {'id': str(q), 'amount': data['amount'], 'category_id': data['category_id'],'description':data['description']}
                    return_data_str = json.dumps(return_data)
                    response = make_response(return_data_str,200)
                    response.headers['Content-Type'] = 'application/json'
                    return response
        else:
            error = {'message': 'content type error'}
            error_str = json.dumps(error)
            response = make_response(error_str, 400)
            response.headers['Content-Type'] = 'application/json'
            return response

    records = mongo.db.records
    q = records.find()
    data = []
    for item in q:
        data.append({'id': item['id'],'amount': item['amount'], 'category_id': item['category_id'],'description':item['description']})

    request_data = json.dumps(data)
    response = make_response(request_data,200)
    response.headers['Content-Type'] = 'application/json'
    return request_data

@app.route('/records/<record_id>',methods=['GET'])
def view_record(record_id):
    # Start Token Checking
    token_key = request.headers.get('Authorization')
    try:
        decoded = jwt.decode(token_key, app.config['SECRET'], algorithms=['HS256'])
    except:
        error = {'message': "Signature expired. Please log in again."}
        error_str = json.dumps(error)
        response = make_response(error_str, 400)
        response.headers['Content-Type'] = 'application/json'
        return response

    blacklisted = mongo.db.blacklisted
    q = blacklisted.find_one({'username': decoded['sub'], 'token': token_key})
    if q:
        error = {'message': "Authentication information is missing or invalid"}
        error_str = json.dumps(error)
        response = make_response(error_str, 400)
        response.headers['Content-Type'] = 'application/json'
        return response
    # End of Token Checking
    records = mongo.db.records
    q = records.find_one({'id':record_id})
    if q:
        request_data = {'id':q['id'],'amount':q['amount'],'category_id':q['category_id'],'description':q['description']}
        request_data_str = json.dumps(request_data)
        response = make_response(request_data_str,200)
        response.headers['Content-Type'] = 'application/json'
        return response
    error = {'message': 'record not found'}
    error_str = json.dumps(error)
    response = make_response(error_str, 404)
    response.headers['Content-Type'] = 'application/json'
    return response


# USER SECTION
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
            password_pattern = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\\w\\s]).{8,}$")
            email_pattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
            username_pattern = re.compile("([a-z]+[_]+[a-z]*)")
            if not password_pattern.match(data['password']):
                error = {"invalid_fields": [{"field": 'password', "reason": "'string' does not match '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\\\\w\\\\s]).{8,}$'"}]}
                error_str = json.dumps(error)
                response = make_response(error_str, 400)
                response.headers['Content-Type'] = 'application/json'
                return response
            if not email_pattern.match(data['email']):
                error = {"invalid_fields": [{"field": 'email',
                                             "reason": "'string' does not match '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'"}]}
                error_str = json.dumps(error)
                response = make_response(error_str, 400)
                response.headers['Content-Type'] = 'application/json'
                return response
            if not username_pattern.match(data['username']):
                error = {"invalid_fields": [{"field": 'username',
                                             "reason": "this only accepts lowercase letter and underscore, and should start with letter"}]}
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
                error = {'message': "there's something wrong when inserting the data"}
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
                generated_token = jwt.encode(payload,app.config['SECRET'],algorithm='HS256')
                return_data = {'token':generated_token.decode('utf-8')}
                return_data_str = json.dumps(return_data)
                response = make_response(return_data_str,200)
                response.headers['Content-Type'] = 'application/json'
                return response

            except Exception as e:
                return e
    error = {'message': "Invalid username or password"}
    error_str = json.dumps(error)
    response = make_response(error_str, 401)
    response.headers['Content-Type'] = 'application/json'
    return response

# user logout
@app.route('/users/logout', methods=['POST'])
def logout():
    # Start Token Checking
    token_key = request.headers.get('Authorization')
    try:
        decoded = jwt.decode(token_key, app.config['SECRET'], algorithms=['HS256'])
    except:
        error = {'message': "Signature expired. Please log in again."}
        error_str = json.dumps(error)
        response = make_response(error_str, 400)
        response.headers['Content-Type'] = 'application/json'
        return response

    blacklisted = mongo.db.blacklisted
    q = blacklisted.find_one({'username': decoded['sub'], 'token': token_key})
    if q:
        error = {'message': "Invalid token"}
        error_str = json.dumps(error)
        response = make_response(error_str, 400)
        response.headers['Content-Type'] = 'application/json'
        return response
    # End of Token Checking


    blacklisted.insert({'username':decoded['sub'],'token':token_key})
    return_data = {'message': 'OK'}
    return_data_str = json.dumps(return_data)
    response = make_response(return_data_str,200)
    return response

# retrieve user
@app.route('/users/<username>',methods=['GET'])
def get_users(username):
    # Start Token Checking
    token_key = request.headers.get('Authorization')
    try:
        decoded = jwt.decode(token_key, app.config['SECRET'], algorithms=['HS256'])
    except:
        error = {'message': "Signature expired. Please log in again."}
        error_str = json.dumps(error)
        response = make_response(error_str, 400)
        response.headers['Content-Type'] = 'application/json'
        return response

    blacklisted = mongo.db.blacklisted
    q = blacklisted.find_one({'username': decoded['sub'], 'token': token_key})
    if q:
        error = {'message': "Authentication information is missing or invalid"}
        error_str = json.dumps(error)
        response = make_response(error_str, 400)
        response.headers['Content-Type'] = 'application/json'
        return response
    # End of Token Checking

    users = mongo.db.users
    q = users.find_one({'username':username})
    if q:
        request_data = {"balance": q['balance'],"email": q['email'],"firstName": q['firstName'],"lastName": q['lastName'],"phone": q['phone'],"username": q['username']}
        request_data = json.dumps(request_data)
        response = make_response(request_data,200)
        return response

    error = {'message':'User not found'}
    error_str = json.dumps(error)
    response = make_response(error_str, 404)
    return response

if __name__ == '__main__':
    app.run()


