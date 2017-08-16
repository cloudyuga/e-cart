from flask import Flask, request, Response
import json
from passlib.hash import sha256_crypt
import os
import logging
from pymongo import MongoClient
import bson.json_util
import random
import jwt

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

client = MongoClient('userdb', 27017)
db = client.userDb

@app.route('/register', methods=['POST'])
def register():
  logger.info("Entered User service to register")
  try:
   logger.info("Authenticating token")
   token = request.headers['access-token']
   logger.debug("Received token: {}".format(token))
   jwt.decode(token, app.config['SECRET_KEY'])
   logger.info("Token authentication successful")
   data = json.loads(request.data)
   username = data['username']
   password = data['password']
   email = data['email']
   while True:
      try:
         logger.info('Inserting into database')
         userId = random.randint(1, 1000)
         userInformation = {'_id': userId, 'username': username, 'password': password, 'email': email}
         logger.debug("User details: {}".format(userInformation))
         db.user.insert(userInformation)
         response = Response(status=200)
         logger.info("Leaving User successfully.")
      except:
         userId = random.randint(1, 1000)
         continue
      break
   return response
  except:
     logger.info("Token authentication failed. Leaving user service")
     response = Response(status=500)
     return response

@app.route('/login', methods=['POST'])
def login():
   logger.info("Entered User service to login")
   try:
    logger.info("Authenticating token")
    token = request.headers['access-token']
    jwt.decode(token, app.config['SECRET_KEY'])
    logger.info("Token authentication successful")
    data = json.loads(request.data)
    username = data['username']
    password_candidate = data['password_candidate']
    logger.debug("Details: {}".format(data))
    try:
       logger.info("Fetching user information")
       userdb = db.user.find_one({'username': username})
       logger.debug("Login: {}".format(userdb))
       userInformation = db.user.find_one({'username': username})
       password = userInformation['password']
       logger.info("Validating password")
       if sha256_crypt.verify(password_candidate, password):
          logger.info("Fetching user Id {}".format(userInformation['_id']))
          userId = userInformation['_id']
          logger.debug("Type of ID: {}".format(type(userId)))
          logger.info("Dumping json")
          userId = json.dumps({"userId": userId})
          logger.info("Setting response {}".format(userId))
          response = Response(status=200, response=userId)
          logger.info("Leaving User service successfully")
       else:
          logger.warning("Passwords do not match. Leaving User Service")
          response = Response(status=401)
    except:
        logger.info("Execution failed. Leaving user service")
        response = Response(status=500)
    return response
   except:
      logger.info("Token authentication failed")
      response = Response(status=500)
      return response

app.run(port=5002, debug=True, host='0.0.0.0')
