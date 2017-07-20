from app import app
from flask import flash, redirect, url_for, session, render_template
from app.config import mysql

@app.route('/addToCart/<int:id>')
def addToCart(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM cart where user_id = {}".format(session['userId']))
    if result == 0:
        cur.execute("INSERT INTO cart(user_id) VALUES ({})".format(session['userId']))
    cur.execute("SELECT * FROM cart where user_id = {}".format(session['userId']))
    data = cur.fetchone()
    cur.execute("INSERT INTO cart_items(cart_id, product_id, quantity) VALUES ({0}, {1}, {2})".format(data['cart_id'], id, 1))
    mysql.connection.commit()
    cur.close()
    flash('You have successfully added this product to your cart','success')
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM cart_items where cart_id in \
                            (SELECT cart_id from cart where user_id={})".format(session['userId']))
    if result > 0:
        cart = cur.fetchall()
        return render_template('cart.html', cart=cart)
    else:
        return "CART EMPTY"
