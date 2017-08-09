from app import app
from flask_mysqldb import MySQL
import os

# app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
# app.config['MYSQL_USER'] = 'sql12186197'
# app.config['MYSQL_PASSWORD'] = 'v1LbHD2jDU'
# app.config['MYSQL_DB'] = 'sql12186197'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = '1234'
#app.config['MYSQL_DB'] = 'ecommerce2'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.config['MYSQL_HOST'] = os.environ['MYSQL_DB_HOST']
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_DB_PASSWORD']
app.config['MYSQL_DB'] = 'ecommerce'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

