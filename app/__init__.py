from flask import Flask


app = Flask(__name__)
from app.home import home
from app.user import register, login
from app.cart import cart
from app.orders import orders
