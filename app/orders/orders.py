from app import app
from flask import session, render_template, request, Response
from app.config import mysql
from app.user.login import is_logged_in
import jwt
import logging
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route('/place-order/<int:cartId>')
@is_logged_in
def placeOrder(cartId):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO orders(cart_id, order_status) VALUES({0}, 'Pending Payment')".format(cartId))
    cur.execute("SELECT * FROM orders where cart_id = {0}".format(cartId))
    data = cur.fetchone()
    orderId = data['order_id']
    if cur.execute("UPDATE cart set state='INACTIVE' WHERE cart_id = {}".format(cartId)):
        mysql.connection.commit()
        cur.close()
        return render_template('place-order.html', orderId=orderId)
    return render_template('No orders')

@app.route('/update-order-status', methods=['POST'])
def updateOrderStatus():
    logger.info("Entered orders to update order status")
    data = json.loads(request.data)
    try:
        logger.info("Updating order status")
        cur = mysql.connection.cursor()
        cur.execute("UPDATE orders SET order_status = 'Amount Paid' WHERE order_id={}".format(data['orderId']))
        mysql.connection.commit()
        cur.close()   
        logger.info("Successfully leaving Orders")
        response = Response(status=200)
    except:
        logger.info("Execution failed. Leaving Orders")
        response = Response(status=500)
    return response

@app.route('/orders')
@is_logged_in
def orders():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM orders WHERE cart_id in \
                    (SELECT cart_id FROM cart WHERE user_id={})".format(session['userId']))
    if result > 0:
        data = cur.fetchall()
        print("DATA = ",data)
        return render_template('orders.html', orders=data)
    return render_template('index.html')
