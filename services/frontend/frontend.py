from flask import Flask, redirect, url_for, render_template, session, request, jsonify, flash
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from forms.register import RegisterForm
from functools import wraps
import logging
import jwt
import requests
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

@app.route('/')
def index():
    logger.info('Entered index method')
    logger.info("Generating token")
    token = jwt.encode({}, app.config['SECRET_KEY'])
    token = token.decode('UTF-8')
    headers = {'access-token': token, 'content-type': 'application/json'}
    url = 'http://catalogue:5001/'
    response = requests.post(url, headers=headers)
    logger.debug('RESPONSE {}'.format( response.status_code))
    if response.status_code is 200:
        products = json.loads(response.content)['productDetails']
        logger.debug('Products returned from catalogue {}'.format(products))
        return render_template('index.html', products=products)
    return render_template('index.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login!', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/register', methods=['GET', 'POST'])
def register():
    logger.info("Entered register method")
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        data = {"email": form.email.data, "username": form.username.data, "password": sha256_crypt.encrypt(str(form.password.data))}
        data = json.dumps(data)
        logger.info("Received form data")
        logger.info("Generating token")
        token = jwt.encode({}, app.config['SECRET_KEY'])
        token = token.decode('UTF-8')
        headers = {'access-token': token, 'content-type': 'application/json'}        
        url = 'http://user:5002/register'
        response = requests.post(url, data=data, headers=headers)
        logger.info("Response from Register: {}".format(response.status_code))
        if response.status_code is 200:
            flash('You are now registered and can login', 'success')
            return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    logger.info("Entered login method")
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']
        data = {"username": username, "password_candidate": password_candidate}
        data = json.dumps(data)
        logger.info("Received form data")
        logger.info("Generating token")
        token = jwt.encode({}, app.config['SECRET_KEY'])
        token = token.decode('UTF-8')
        headers = {'access-token': token, 'content-type': 'application/json'}
        url = 'http://user:5002/login'
        response = requests.post(url, data=data, headers=headers)
        logger.debug("Reponse from Login: {}".format(response.status_code))
        if response.status_code is 200:
            content = json.loads(response.content)
            session['userId'] = content['userId']
            session['logged_in'] = True
            flash('You are now logged in', 'success')
            return redirect(url_for('index'))
        else:
            error = 'Invalid login'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
@is_logged_in
def logout():
    logger.info("Clearing session")
    session.clear()
    flash("You have been logged out", 'success')
    return redirect(url_for('login'))

@app.route('/add-to-cart/<int:id>')
@is_logged_in
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
    logger.info("Making a request on Cart service")
    url = 'http://cart:5003/add-to-cart'
    response = requests.post(url, data=data, headers=headers)
    logger.debug("Response from Cart: {}".format(response.status_code))
    if response.status_code is 200:
        flash('You have successfully added this product to your cart','success')
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/cart')
@is_logged_in
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

@app.route('/place-order/<int:cartId>')
@is_logged_in
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
@is_logged_in
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
@is_logged_in
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

app.run(port=5000, debug=True, host='0.0.0.0')
