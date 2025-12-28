# extensions.py
from flask_pymongo import PyMongo
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
mongo = PyMongo() # Named db to mongo for clarity
ma = Marshmallow()
jwt = JWTManager()