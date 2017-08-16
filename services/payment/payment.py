from flask import Flask, request, Response, jsonify
import json
import requests
import os
import logging
import random
from pymongo import MongoClient
import jwt

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

client = MongoClient('paymentdb', 27017)
db = client.paymentDb

@app.route('/payment', methods=['POST'])
def payment():
   logger.info("Entered Payment service to make payment")
   try:
    logger.info("Authenticating token")
    token = request.headers['access-token']
    jwt.decode(token, app.config['SECRET_KEY'])
    logger.info("Token authentication successful")
    data = json.loads(request.data)
    try:
       while True:
            try:
               logger.info("Creating new payment")
               paymentId = random.randint(1, 1000)
               db.payment.insert({'_id': paymentId, 'order_id': data['orderId']})
            except:
               continue
            break
        
       headers = {'content-type': 'application/json'}
       url = 'http://orders:5004/update-order-status'
       data = {"orderId": data['orderId']}
       data = json.dumps(data) 
       logger.info("Making a request to Orders to update order status")
       response = requests.post(url, data=data, headers=headers)
       logger.debug("Response from orders: {}".format(response.status_code))
       if response.status_code is 200:
           logger.info("Leaving Payment successfully")
           response = Response(status=200)
           return response
       else:
           logger.info("Failed to update order status. Leaving Payment")
           response = Response(status=500)
           return response
    except:
        logger.info("Execution on Payment failed. Leaving Payment")
        response = Response(status=500)
        return response

   except:
      logger.info("Token authentication failed")
      response = Response(status=500)
      return response


app.run(port=5005, debug=True, host='0.0.0.0')
