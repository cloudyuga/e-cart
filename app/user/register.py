from app import app
from app.forms.register import RegisterForm
from flask import request, render_template, flash, redirect, url_for
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from app.config import mysql

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user(username, password, email, type) VALUES (%s, %s, %s, %s)", (username, password, email, "customer"))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can login', 'success')

        return redirect(url_for('index'))
    return render_template('register.html', form=form)
