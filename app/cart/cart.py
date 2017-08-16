from app import app
from flask import flash, redirect, url_for, session, render_template
from app.config import mysql
from app.user.login import is_logged_in


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
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM cart_items where cart_id in \
                            (SELECT cart_id from cart where user_id={} and state = 'ACTIVE')".format(session['userId']))
    if result > 0:
        cart = cur.fetchall()
        cur.execute("SELECT total_price FROM cart where cart_id = {}".format(cart[0]['cart_id']))
        totalPrice = cur.fetchone()
        totalPrice = totalPrice['total_price']
        return render_template('cart.html', cart=cart, totalPrice=totalPrice)
    else:
        return render_template('cart-empty.html')
