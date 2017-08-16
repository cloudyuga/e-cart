from app import app
from app.config import mysql
from flask import redirect, url_for, render_template, session, request, jsonify, flash
import logging
import jwt
import requests
import json

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
    productId = id
    data = {"productId": productId, "userId": session['userId']}
    data = json.dumps(data)
    logger.info("Received product ID")
    logger.info("Generating token")
    token = jwt.encode({}, app.config['SECRET_KEY'])
    token = token.decode('UTF-8')
    headers = {'access-token': token, 'content-type': 'application/json'}
    url = 'http://cart:5003/add-to-cart'
    response = requests.post(url, data=data, headers=headers)
    logger.debug("Response from Cart: {}".format(response.status_code))
    if response.status_code is 200:
        flash('You have successfully added this product to your cart','success')
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    logger.info("Entered cart method")
    logger.info("Generating token")
    token = jwt.encode({}, app.config['SECRET_KEY'])
    token = token.decode('UTF-8')
    headers = {'access-token': token, 'content-type': 'application/json'}
    url = 'http://cart:5003/cart'
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
    logger.info("Generating token")
    token = jwt.encode({}, app.config['SECRET_KEY'])
    token = token.decode('UTF-8')
    headers = {'access-token': token, 'content-type': 'application/json'} 
    url = 'http://orders:5004/place-order'
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
     data = {"userId": session['userId']}
     data = json.dumps(data)
     logger.info("Generating token")
     token = jwt.encode({}, app.config['SECRET_KEY'])
     token = token.decode('UTF-8')
     headers = {'access-token': token, 'content-type': 'application/json'}
     url = 'http://cart:5003/get-all-cart-id'
     response = requests.post(url, data=data, headers=headers)
     logger.debug("Response from Cart: {}".format(response.status_code))
     if response.status_code is 200:
        data = response.content 
        url = 'http://orders:5004/orders'
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
    orderId = id
    logger.info("Generating token")
    token = jwt.encode({}, app.config['SECRET_KEY'])
    token = token.decode('UTF-8')
    headers = {'access-token': token, 'content-type': 'application/json'}
    url = 'http://payment:5005/payment'
    data = {"orderId": orderId}
    data = json.dumps(data)
    response = requests.post(url, data=data, headers=headers)
    logger.debug("Response from Payment: {}".format(response.status_code))
    if response.status_code is 200:
        logger.info("Rendering payment page")
        return render_template('payment.html')
    return render_template('payment-failure.html')
