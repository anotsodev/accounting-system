from flask import Flask, request, make_response, json
from passlib.hash import sha256_crypt
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)