from app import app
from flask_mysqldb import MySQL

app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql12186197'
app.config['MYSQL_PASSWORD'] = 'v1LbHD2jDU'
app.config['MYSQL_DB'] = 'sql12186197'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
