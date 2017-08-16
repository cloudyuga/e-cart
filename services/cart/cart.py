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

client = MongoClient('cartdb', 27017)
db = client.cartDb

@app.route('/add-to-cart', methods=['POST'])
def addToCart():
  logger.info("Entered Cart service to add a product to cart")
  try:
   logger.info("Authenticating token")
   token = request.headers['access-token']
   jwt.decode(token, app.config['SECRET_KEY'])
   logger.info("Token authentication successful")
   data = json.loads(request.data)
   try:
      logger.info("Checking if cart exisits")
      cart = db.cart.find_one({'user_id': data['userId'], 'state': 'ACTIVE'})
      if cart is None:
         while True:
            try:
               logger.info("Creating new cart")
               cartId = random.randint(1, 1000)
               db.cart.insert({'_id': cartId, 'user_id': data['userId'], 'total_price': 0, 'state': 'ACTIVE'})
            except:
               continue
            logger.info("Fetching cart details")
            cart = db.cart.find_one({'user_id': data['userId'], 'state': 'ACTIVE'})
            break
      logger.info("Fetchin cart ID")
      cartId = cart['_id']
      while True:
         try:
            logger.info("Inserting into cart items")
            cartItemsId = random.randint(1, 1000)
            db.cart_items.insert({'_id': cartItemsId, 'cart_id': cartId, 'product_id': data['productId'], 'quantity': 1})
         except:
            continue
         break
      logger.info("Making a request on Catalogue service to obtain the price of the product")
      headers = {'content-type': 'application/json'}
      url = 'http://app:5000/price'
      data = {"productId": data['productId']}
      data = json.dumps(data)
      response = requests.post(url, data=data, headers=headers)        
      logger.info("Response from Catalogue: {}".format(response.status_code))
      if response.status_code is 200:
         data = json.loads(response.content)
         logger.info("Updating total price of cart")
         db.cart.update({'_id': cartId}, {'$inc': {'total_price': data['price']}})
      else:
         response.status = 500
         return response
      logger.info("Leaving Cart successfully")
      response = Response(status=200)
      return response
   except:
      logger.debug("Execution failed. Leaving Cart service")
      response = Response(status=500)
      return response
  except:
     logger.info("Token authentication failed")
     response = Response(status=500)
     return response

@app.route('/cart', methods=['POST'])
# ToDo: List products and remove duplication of cart items, handle case for result zero
def cart():
   logger.info("Entered Cart service to display cart items")
   try:
    logger.info("Authenticating token")
    token = request.headers['access-token']
    jwt.decode(token, app.config['SECRET_KEY'])
    logger.info("Token authentication successful")
    data = json.loads(request.data)
    try:
       logger.info("Loading cart")
       cart = db.cart.find_one({'user_id': data['userId'], 'state': 'ACTIVE'})
       if cart is not None:
          cartId = cart['_id']
          logger.info("Loading cart items")
          cartItems = list(db.cart_items.find({'cart_id': cartId}))
          logger.info("Fetching total price")
          totalPrice = db.cart.find_one({'_id': cartId})['total_price']
          data = {'cart': cartItems, 'totalPrice': totalPrice}
          return(jsonify(data)), 200
    except:
        logger.info("Execution failed. Leaving cart service")
        response = Response(status=500)
        return response
   except:
      logger.info("Token authentication failed")
      response = Response(status=500)
      return response

@app.route('/get-all-cart-id', methods=['POST'])
def getCartId():
    logger.info("Entered Cart to fetch user's cart IDs")
    data = json.loads(request.data)
    try:
       logger.info("Loading cart Ids")
       cartIds = []
       carts = list(db.cart.find({'user_id': data['userId']}))
       for cart in carts:
          cartIds.append(cart['_id'])
       logger.debug("CartIds: {}".format(cartIds))
       data = {'cartIds': cartIds}
       logger.info("Leaving cart successfully")
       return jsonify(data), 200
    except:
        logger.info("Execution failed. Leaving cart")
        return 500


@app.route('/change-state', methods=['POST'])
def changestate():
   logger.info("Entered Cart service to change state")
   data = json.loads(request.data)
   try:
      logger.info("Setting cart to inactive state")
      db.cart.update({'_id': data['cartId']}, {'$set': {'state': 'INACTIVE'}})
      logger.info("Leaving Cart successfully")
      response = Response(status=200)
   except:
      logger.info("Failed to update cart state. Leaving Cart.")
      response = Response(status=500)
   return response

app.run(port=5003, debug=True, host='0.0.0.0')
