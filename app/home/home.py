from app import app
from app.config import mysql
from flask import redirect, url_for, render_template, session, request, jsonify, flash
import logging
import jwt
import requests
import json
import os
import yaml

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * from product")
    products = cur.fetchall()
    print("PRODUCT = ",products)
    return render_template('index.html', products=products)

@app.route('/add-to-cart/<int:id>')
def addToCart(id):
    logger.info("Entered add to cart method")
    directoryPath = os.path.dirname(os.path.realpath(__file__))
    with open("%s/../endpoints.yaml" % directoryPath, 'r') as stream:
         addToCartUrl = yaml.load(stream)['addToCartUrl']
    productId = id
    data = {"productId": productId, "userId": session['userId']}
    data = json.dumps(data)
    logger.info("Received product ID")
    logger.info("Generating token")
    token = jwt.encode({}, app.config['SECRET_KEY'])
    token = token.decode('UTF-8')
    headers = {'access-token': token, 'content-type': 'application/json'}
    url = addToCartUrl
    response = requests.post(url, data=data, headers=headers)
    logger.debug("Response from Cart: {}".format(response.status_code))
    if response.status_code is 200:
        flash('You have successfully added this product to your cart','success')
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    logger.info("Entered cart method")
    directoryPath = os.path.dirname(os.path.realpath(__file__))
    with open("%s/../endpoints.yaml" % directoryPath, 'r') as stream:
         cartUrl = yaml.load(stream)['cartUrl']
    logger.info("Generating token")
    token = jwt.encode({}, app.config['SECRET_KEY'])
    token = token.decode('UTF-8')
    headers = {'access-token': token, 'content-type': 'application/json'}
    url = cartUrl
    data = {"userId": session['userId']}
    data = json.dumps(data)
    logger.info("Received logged in user's ID")
    response = requests.post(url, data=data, headers=headers)
    logger.debug("Response from cart: {}".format(response.status_code))
    if response.status_code is 200:
        logger.info("Loading cart items")
        cart = json.loads(response.content)['cart']
        logger.info("Loading total price")
        totalPrice = json.loads(response.content)['totalPrice']
        return render_template('cart.html', cart=cart, totalPrice= totalPrice)
    return render_template('cart-empty.html')

@app.route('/price', methods=['POST'])
def price():
   logger.info("Entered the Catalogue service to fetch price of products")
   data = json.loads(request.data)
   productId = data['productId']
   logger.debug("Product ID: {}".format(productId))
   try:
      cur = mysql.connection.cursor()
      logger.debug("Executing query")
      cur.execute("SELECT price FROM product WHERE product_id={}".format(productId))
      logger.info("Executed query")
      result = cur.fetchone()
      logger.info("Fetched row")
      price = result['price']
      logger.debug("Price = {}".format(price))
      return jsonify({"price": price}), 200
   except:
      logger.warning("Execution failed")
      return 500

@app.route('/place-order/<int:cartId>')
def placeOrder(cartId):
    logger.info('Entered place order method')
    directoryPath = os.path.dirname(os.path.realpath(__file__))
    with open("%s/../endpoints.yaml" % directoryPath, 'r') as stream:
         placeOrderUrl = yaml.load(stream)['placeOrderUrl']
    logger.info("Generating token")
    token = jwt.encode({}, app.config['SECRET_KEY'])
    token = token.decode('UTF-8')
    headers = {'access-token': token, 'content-type': 'application/json'} 
    url = placeOrderUrl
    data = {"cartId": cartId}
    data = json.dumps(data)
    logger.info("Loaded cart ID")
    response = requests.post(url, data=data, headers=headers)
    logger.debug('Response from Order: {}'.format(response.status_code))
    if response.status_code is 200:
        logger.info("Loading order ID from response")
        orderId = json.loads(response.content)['orderId']
        logger.info("Rendering place order page")
        return render_template('place-order.html', orderId=orderId)
    return render_template('error.html')

@app.route('/orders')
def orders():
     logger.info("Entered orders method")
     directoryPath = os.path.dirname(os.path.realpath(__file__))
     with open("%s/../endpoints.yaml" % directoryPath, 'r') as stream:
         ordersUrl = yaml.load(stream)['ordersUrl']
     with open("%s/../endpoints.yaml" % directoryPath, 'r') as stream:
         getAllCartIdUrl = yaml.load(stream)['getAllCartIdUrl']        
     data = {"userId": session['userId']}
     data = json.dumps(data)
     logger.info("Generating token")
     token = jwt.encode({}, app.config['SECRET_KEY'])
     token = token.decode('UTF-8')
     headers = {'access-token': token, 'content-type': 'application/json'}
     url = getAllCartIdUrl
     response = requests.post(url, data=data, headers=headers)
     logger.debug("Response from Cart: {}".format(response.status_code))
     if response.status_code is 200:
        data = response.content 
        url = ordersUrl
        response = requests.post(url, data=data, headers=headers)
        logger.debug("Response from Orders: {}".format(response.status_code))
        if response.status_code is 200:
           data = json.loads(response.content)
           logger.debug("Data from Orders: {}".format(data)) 
           return render_template('orders.html', orders=data)
     return render_template('index.html')

@app.route('/payment/<int:id>')
def payment(id):
    logger.info("Entered payment method")
    directoryPath = os.path.dirname(os.path.realpath(__file__))
    with open("%s/../endpoints.yaml" % directoryPath, 'r') as stream:
         paymentUrl = yaml.load(stream)['paymentUrl']
    orderId = id
    logger.info("Generating token")
    token = jwt.encode({}, app.config['SECRET_KEY'])
    token = token.decode('UTF-8')
    headers = {'access-token': token, 'content-type': 'application/json'}
    url = paymentUrl
    data = {"orderId": orderId}
    data = json.dumps(data)
    response = requests.post(url, data=data, headers=headers)
    logger.debug("Response from Payment: {}".format(response.status_code))
    if response.status_code is 200:
        logger.info("Rendering payment page")
        return render_template('payment.html')
    return render_template('payment-failure.html')
