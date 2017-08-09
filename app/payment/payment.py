from app import app
from flask import session, render_template
from app.config import mysql
from app.user.login import is_logged_in

@app.route('/payment/<int:orderId>')
@is_logged_in
def payment(orderId):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO payment(order_id) VALUES({})".format(orderId))
    if cur.execute("UPDATE orders SET order_status = 'Amount Paid' WHERE order_id={}".format(orderId)):
        mysql.connection.commit()
        cur.close()
        return render_template('payment.html')
    return render_template('Payment Failed')
