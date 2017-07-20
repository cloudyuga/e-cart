from app import app
from flask_mysqldb import MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'ecommerce'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
