from app import app
from app.config import mysql
from flask import render_template
from app.cart.cart import addToCart, getAllCartId
import logging
import jwt
import requests
import json
import yaml
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * from product")
    products = cur.fetchall()
    print("PRODUCT = ",products)
    return render_template('index.html', products=products)


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
     directoryPath = os.path.dirname(os.path.realpath(__file__))        
     with open("%s/../endpoints.yaml" % directoryPath, 'r') as stream:
         ordersUrl = yaml.load(stream)['ordersUrl']
     token = jwt.encode({}, app.config['SECRET_KEY'])
     token = token.decode('UTF-8')
     headers = {'access-token': token, 'content-type': 'application/json'}
     cartIds = getAllCartId()
     logger.debug("Received cart ID: {}".format(cartIds))
     data = {"cartIds": cartIds}
     data = json.dumps(data)
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
    orderId = id
    logger.info("Generating token")
    with open("%s/../endpoints.yaml" % directoryPath, 'r') as stream:
         paymentUrl = yaml.load(stream)['paymentUrl']
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
