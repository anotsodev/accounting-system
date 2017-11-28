import json
from flask import Flask, request, redirect, url_for, jsonify
import requests
from flask import make_response

app = Flask(__name__)

url = 'http://localhost:5000'
api_path = '/'

@app.route("/", methods = ['GET'])
def index():
    return '''
        <html>
            <a href="/register">register</a>
        </html>
    '''

# User Management
@app.route("/register", methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        data = {}
        for r in request.form:
            data.update({r: request.form[r]})
        post_data = json.dumps(data)
        print (post_data)
        headers = {'Accept': 'application/json'}
        r = requests.post(url+api_path+'users', data=post_data, headers=headers)
        print (r.text)
        return redirect(url_for('index'))
    return '''
            <form method="post">
                <p>Username <input type=text name=username>
                <p>Password <input type=text name=password>
                <p>First Name <input type=text name=firstName>
                <p>Last Name <input type=text name=lastName>
                <p>Email <input type=text name=email>
                <p>Phone <input type=text name=phone>
                <p>Balance <input type=text name=balance>
                <p>Submit <input type=submit value=submit>
            </form>
        '''

@app.route('/login',methods=['GET','POST'])
def login():
    pass

@app.route('/users/<username>',methods=['GET'])
def get_user_info():
    pass

@app.route('/logout',methods=['POST'])
def logout():
    pass

# Records Management



# Categories Management

if __name__ == '__main__':
    app.run(port=8080)