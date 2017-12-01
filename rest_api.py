from flask import Flask, request, make_response, json
from passlib.hash import sha256_crypt
from flask_pymongo import PyMongo
from flask_cors import CORS
import jwt
import datetime
import base64
import re
import uuid

app = Flask(__name__)
CORS(app)

app.config['MONGO_DBNAME'] = 'accounting-system'
app.config['SECRET'] = 'secret' # change this
mongo = PyMongo(app)

# CATEGORY SECTION
@app.route('/categories',methods=['GET','POST'])
def categories():
    # Start Token Checking
    token_key = request.headers.get('Authorization')
    try:
        decoded = jwt.decode(token_key, app.config['SECRET'], algorithms=['HS256'])
    except:
        error = {'message': "Invalid token."}
        error_str = json.dumps(error)
        response = make_response(error_str, 400)
        response.headers['Content-Type'] = 'application/json'
        return response

    blacklisted = mongo.db.blacklisted
    q = blacklisted.find_one({'username': decoded['sub'], 'token': token_key})
    if q:
        error = {'message': "Invalid token."}
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
            if "name" not in data.keys():
                error = {'message': 'invalid request body'}
                error_str = json.dumps(error)
                response = make_response(error_str, 400)
                response.headers['Content-Type'] = 'application/json'
                return response
            if "type" not in data.keys():
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
                accounts = mongo.db.accounts
                q = accounts.find_one({'categories.name':data['name'],'category.type':data['type']})
                print(data['name'])
                if q:
                    error = {'message': data['name']+" is already in the categories"}
                    error_str = json.dumps(error)
                    response = make_response(error_str, 400)
                    response.headers['Content-Type'] = 'application/json'
                    return response

                unique_id = uuid.uuid1()
                data.update({'id':str(unique_id)})
                username = decoded['sub']
                q = accounts.update({"username" : username},{"$addToSet": {"categories":data}})
                if q:
                    return_data = {"id":unique_id,"name":data['name'],"type":data['type']}
                    return_data_str = json.dumps(return_data)
                    response = make_response(return_data_str,200)
                    response.headers['Content-Type'] = 'application/json'
                    return response
        else:
        # if request content-type is not json, this will return an error response
            error = {"detail": "Invalid Content-type (application/json), expected JSON data","status": 415,"title": "Unsupported Media Type","type": "about:blank"}
            error_str = json.dumps(error)
            response = make_response(error_str, 415)
            response.headers['Content-Type'] = 'application/json'
            return response

    # this will return all the categories if the method is not POST
    # by default the method is GET
    accounts = mongo.db.accounts
    username = decoded['sub']
    q = accounts.find_one({'username':username})
    request_data = json.dumps(q['categories'])
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
        error = {'message': "Invalid token."}
        error_str = json.dumps(error)
        response = make_response(error_str, 400)
        response.headers['Content-Type'] = 'application/json'
        return response
    # End of Token Checking
    # This will check the category if the category id is same with the request category id
    # this will simply search categories collection with the given category id
    accounts = mongo.db.accounts
    username = decoded['sub']
    q = accounts.find_one({'username':username})
    for s in q['categories']:
        if s['id'] == category_id:
            request_data = s
            request_data_str = json.dumps(request_data)
            response = make_response(request_data_str, 200)
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
    username = ""
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
        error = {'message': "Invalid token."}
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
                accounts = mongo.db.accounts
                username = decoded['sub']
                unique_id = uuid.uuid1()
                data.update({'id': str(unique_id)})
                type = ""
                q = accounts.find_one({'username':username})
                for y in q['categories']:
                    if y['id'] == data['category_id']:
                        type = y['type']

                if type == "income":
                    try:
                        accounts.update({"username" :username},{"$inc" : {'balance':float(data['amount'])}})
                    except:
                        error = {'message': 'invalid amount input'}
                        error_str = json.dumps(error)
                        response = make_response(error_str, 404)
                        response.headers['Content-Type'] = 'application/json'
                        return response

                if type == "expense":
                    q_bal = accounts.find_one({'username':username})
                    balance = float(q_bal['balance'] - int(data['amount']))
                    accounts.update({"username": username}, {"$set": {'balance': balance}})

                all_categories = [x['id'] for x in q['categories']]

                if data['category_id'] in all_categories:
                    q = accounts.update({"username": username}, {"$addToSet": {"records": data}})
                    return_data = {'id': unique_id, 'amount': data['amount'], 'category_id': data['category_id'],
                                   'description': data['description']}

                    return_data_str = json.dumps(return_data)
                    response = make_response(return_data_str, 200)
                    response.headers['Content-Type'] = 'application/json'
                    return response
                else:
                    error = {'message': 'category not found'}
                    error_str = json.dumps(error)
                    response = make_response(error_str, 404)
                    response.headers['Content-Type'] = 'application/json'
                    return response
        else:
            error = {"detail": "Invalid Content-type (application/json), expected JSON data","status": 415,"title": "Unsupported Media Type","type": "about:blank"}
            error_str = json.dumps(error)
            response = make_response(error_str, 415)
            response.headers['Content-Type'] = 'application/json'
            return response


    accounts = mongo.db.accounts
    username = decoded['sub']
    q = accounts.find_one({'username': username})
    request_data = json.dumps(q['records'])
    response = make_response(request_data,200)
    response.headers['Content-Type'] = 'application/json'
    return request_data

@app.route('/records/<record_id>',methods=['GET','DELETE'])
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
        error = {'message': "Invalid token."}
        error_str = json.dumps(error)
        response = make_response(error_str, 400)
        response.headers['Content-Type'] = 'application/json'
        return response
    # End of Token Checking
    if request.method == 'DELETE':
        accounts = mongo.db.accounts
        username = decoded['sub']
        q = accounts.find_one({'username': username})
        for s in q['records']:
            if s['id'] == record_id:
                request_data = s
                request_data_str = json.dumps(request_data)
                response = make_response(request_data_str, 200)

                accounts.update({'username': username},
                                {"$pull": {"records": {"id": record_id}}}, False, True)

                response.headers['Content-Type'] = 'application/json'

                return response
    accounts = mongo.db.accounts
    username = decoded['sub']
    q = accounts.find_one({'username':username})
    for s in q['records']:
        if s['id'] == record_id:
            request_data = s
            request_data_str = json.dumps(request_data)
            response = make_response(request_data_str, 200)
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
        required = ['username','password','firstName','lastName','email', 'balance', 'phone']
        incomplete = False
        error = {"invalid_fields":[]}
        for r in required:
            if r not in data.keys():
                error["invalid_fields"].append({"field": r, "reason": r + " is a required property"})
                incomplete = True

        if incomplete:
            error_str = json.dumps(error)
            response = make_response(error_str, 400)
            response.headers['Content-Type'] = 'application/json'
            return response

        else:
            # check password if in pattern, return 400 response error if not match, else continue
            error = {"invalid_fields":[]}
            incomplete = False
            password_pattern = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\\w\\s]).{8,}$")
            email_pattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
            username_pattern = re.compile("([a-z]+[_]+[a-z]*)")

            if not username_pattern.match(data['username']):
                error["invalid_fields"].append({"field": 'username',
                                             "reason": "usernames must only have lowercase letters and underscore. Example: john_doe"})
                incomplete = True
            if not password_pattern.match(data['password']):
                error["invalid_fields"].append({"field": 'password', "reason": "password does not match '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\\\\w\\\\s]).{8,}$'"})
                incomplete = True
            if not email_pattern.match(data['email']):
                error["invalid_fields"].append({"field": 'email',
                                             "reason": "email does not match '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'"})
                incomplete = True
            if data['balance'] == "":
                data['balance'] = 0.0
            else:
                data['balance'] = float(data['balance'])
            if incomplete:
                error_str = json.dumps(error)
                response = make_response(error_str, 400)
                response.headers['Content-Type'] = 'application/json'
                return response

        # Insert database section
        # Encrypt password
        hashed_password = sha256_crypt.hash(data['password'])
        data['password'] = hashed_password

        # check for existing user
        accounts = mongo.db.accounts
        q = accounts.find_one({'username':data['username']})
        if q:
            error = {"invalid_fields": [{"field": 'username',
                                         "reason": "User "+data['username']+" already existed"}]}
            error_str = json.dumps(error)
            response = make_response(error_str, 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            data.update({'categories':[],'records':[]})
            if mongo.db.accounts.insert(data):
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
        error = {"detail": "Invalid Content-type (application/json), expected JSON data","status": 415,"title": "Unsupported Media Type","type": "about:blank"}
        error_str = json.dumps(error)
        response = make_response(error_str, 415)
        response.headers['Content-Type'] = 'application/json'
        return response

# user login
@app.route('/users/login', methods=['POST'])
def login_user():
    try:
        basic_auth = request.headers.get("Authorization")
        basic_auth = basic_auth.replace("Basic","")
        basic_auth = base64.b64decode(basic_auth)
        basic_auth = basic_auth.decode('utf-8')
    except:
        error = {'message': "Invalid username or password"}
        error_str = json.dumps(error)
        response = make_response(error_str, 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if ':' not in basic_auth:
        error = {'message': "Invalid username or password"}
        error_str = json.dumps(error)
        response = make_response(error_str, 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    accounts = mongo.db.accounts
    username = basic_auth.split(':')[0]
    password = basic_auth.split(':')[1]
    q = accounts.find_one({'username':username})
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
        error = {'message': "Invalid token."}
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
        error = {'message': "Invalid token."}
        error_str = json.dumps(error)
        response = make_response(error_str, 400)
        response.headers['Content-Type'] = 'application/json'
        return response
    # End of Token Checking

    accounts = mongo.db.accounts
    q = accounts.find_one({'username':username})
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
    # default port is 5000
    app.run(host= '0.0.0.0')


