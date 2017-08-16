from app import app
from flask import flash, redirect, url_for, session, render_template, Response, request
from app.config import mysql
from app.user.login import is_logged_in
import logging
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route('/addToCart/<int:id>')
@is_logged_in
def addToCart(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM cart where user_id = {} and state = 'ACTIVE'".format(session['userId']))
    if result == 0:
        cur.execute("INSERT INTO cart(user_id, total_price, state) VALUES ({}, 0, 'ACTIVE')".format(session['userId']))
    cur.execute("SELECT * FROM cart where user_id = {} and state = 'ACTIVE'".format(session['userId']))
    data = cur.fetchone()
    cur.execute("INSERT INTO cart_items(cart_id, product_id, quantity) VALUES ({0}, {1}, {2})".format(data['cart_id'], id, 1))
    cur.execute("UPDATE cart,product SET cart.total_price=cart.total_price+product.price WHERE product.product_id={}".format(id))
    mysql.connection.commit()
    cur.close()
    flash('You have successfully added this product to your cart','success')
    return redirect(url_for('index'))


@app.route('/cart')
@is_logged_in
def cart():
   logger.info("Requesting for cart ID")
   cartId = getActiveCartId()
   if cartId != None:
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM cart_items where cart_id={}".format(cartId))
    if result > 0:
        cart = cur.fetchall()
        cur.execute("SELECT total_price FROM cart where cart_id = {}".format(cart[0]['cart_id']))
        totalPrice = cur.fetchone()
        totalPrice = totalPrice['total_price']
        return render_template('cart.html', cart=cart, totalPrice=totalPrice)
    else:
        return render_template('cart-empty.html')
   else:
       return render_template('cart-empty.html')

def getActiveCartId():
   logger.info("Entered method to obtain cart ID")
   cur = mysql.connection.cursor()
   try:
      logger.info("Created cursor")
      logger.debug("Logged in user ID: {}".format(session['userId']))
      cur.execute("SELECT cart_id from cart where user_id={} and state='ACTIVE'".format(session['userId']))
      logger.info("Executed query")
      result = cur.fetchone()
      logger.info("Fetched id row")
      cartId = result['cart_id']
      logger.debug("Cart ID = {}".format(cartId))
      cur.close()
      return cartId
   except:
      return None

def getAllCartId():
   cur = mysql.connection.cursor()
   logger.info("Entered method to obtain all carts of the user")
   logger.info("Created cursor")
   logger.debug("Logged in user ID: {}".format(session['userId']))
   cur.execute("SELECT cart_id from cart where user_id={}".format(session['userId']))
   logger.info("Fetched Cart Ids")
   cartIds = list(cur.fetchall())
   logger.debug("Cart Ids: {}".format(cartIds))
   return cartIds

@app.route('/change-state', methods=['POST'])
def changeState():
   logger.info("Entered Cart service to change state")
   cur = mysql.connection.cursor()
   data = json.loads(request.data)
   try:
      logger.info("Setting cart to inactive state")
      cur = mysql.connection.cursor()
      if cur.execute("UPDATE cart set state='INACTIVE' WHERE cart_id = {}".format(data['cartId'])):
         mysql.connection.commit()
         cur.close()
         logger.info("Updated cart state. Leaving cart successfully")
         response = Response(status=200)
   except:
        logger.info("Execution failed. Leaving Orders")
        response = Response(status=500)
   return response
