from app import app
from flask_mysqldb import MySQL
import os

app.config['SECRET_KEY'] = 'secret'

mysql = MySQL(app)

