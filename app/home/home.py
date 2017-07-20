from app import app
from app.config import mysql
from flask import render_template
from app.cart.cart import addToCart

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * from product")
    products = cur.fetchall()
    print("PRODUCT = ",products)
    return render_template('index.html', products=products)
