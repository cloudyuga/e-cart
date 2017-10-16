from app import app
from app.config import mysql
from flask import render_template
from app.cart.cart import addToCart
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

@app.route('/payment/<int:id>')
def payment(id):
    directoryPath = os.path.dirname(os.path.realpath(__file__))
    logger.info("Entered payment method")
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
