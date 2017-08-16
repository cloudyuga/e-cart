from flask import Flask, request, Response, jsonify
import json
import os
import logging
import requests
import random
from pymongo import MongoClient
import jwt

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

client = MongoClient('ordersdb', 27017)
db = client.ordersDb

@app.route('/place-order', methods=['POST'])
def placeOrder():
   logger.info("Entered Order service to place an order")
   try:
    logger.info("Authenticating token")
    token = request.headers['access-token']
    jwt.decode(token, app.config['SECRET_KEY'])
    logger.info("Token authentication successful")
    data = json.loads(request.data)
    logger.debug("Received data: {}".format(data))
    try:
     while True:
       try:
          logger.info("Generating order ID")
          ordersId = random.randint(1, 1000)
          db.orders.insert({'_id': ordersId, 'cart_id': data['cartId'], 'order_status': 'Pending Payment'})
       except:
          continue
       break
     logger.info("Fetching order")
     order = db.orders.find_one({'cart_id': data['cartId']})
     headers = {'content-type': 'application/json'} 
     data = json.dumps(data)
     url = 'http://app:5000/change-state'
     logger.info("Making a request to Cart to change the cart state")
     response = requests.post(url, data=data, headers=headers)
     logger.debug("Response from Cart: {}".format(response.status_code))
     if response.status_code is 200:
       logger.info("Returning order Id successfully")
       data = {"orderId": order['_id']}
       return jsonify(data), 200
     else:
       logger.info("Execution Failed on Cart. Leaving Order.")
       return 500
    except:
       logger.info("Execution failed. Leaving order")
       response = Response(status=500)
       return response
   except:
      logger.info("Token authentication failed")
      response = Response(status=500)
      return response



@app.route('/update-order-status', methods=['POST'])
def updateOrderStatus():
    logger.info("Entered orders to update order status")
    data = json.loads(request.data)
    try:
        logger.info("Updating order status")
        db.orders.update({'_id': data['orderId']}, {'$set': {'order_status': 'Amount Paid'}})
        logger.info("Sunncessfully leaving Orders")
        response = Response(status=200)
    except:
        logger.info("Execution failed. Leaving Orders")
        response = Response(status=500)
    return response

@app.route('/orders', methods=['POST'])
def orders():
   logger.info("Entering Orders service to fetch order details")
   try:
    logger.info("Authenticating token")
    token = request.headers['access-token']
    jwt.decode(token, app.config['SECRET_KEY'])
    logger.info("Token authentication successful")
    data = json.loads(request.data)
    logger.debug("Data received: {}".format(data))
    orders = []
    try:
       logger.info("Fetching all orders")
       for cartId in data['cartIds']:
          logger.debug("Cart ID: {}".format(cartId))
          order = db.orders.find_one({'cart_id': cartId['cart_id']})
          logger.debug("Order: {}".format(order))
          orders.append(order)
       logger.debug("Orders: {}".format(orders))
       logger.info("Leaving orders successfully")
       return jsonify(orders), 200
    except:
       return 500
   except:
      logger.info("Token authentication failed")
      response = Response(status=500)
      return response

app.run(port=5004, debug=True, host='0.0.0.0')
