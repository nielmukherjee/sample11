from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
import os
import subprocess

import database

app = Flask(__name__)
app.secret_key = "major project secret key"


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/dashboard')
def dashboard():
    return render_template('new_dashboard.html')

@app.route('/profile')
def profile():
    return render_template('Profile.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    errors = ''
    print('run')
    if request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('password')
        if username and password:
            db = database.Database()
            userlist = db.view_user()
            print(userlist)
            for row in userlist:
                if username in row and password in row:
                    session['id'] = row[0]
                    session['username'] = row[1]
                    session['logged_in'] = True
                    message = "successful logged in"
                    return redirect(url_for('dashboard', data=message))
            errors = "invalid credential"
        else:
            errors = "please fill details"
    return render_template('login.html', errors=errors)


@app.route('/register', methods=['GET', 'POST'])
def register():
    errors = ""
    if request.method == 'POST':
        db = database.Database()
        try:
            db.user_table()
        except:
            pass
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('pwd')
        cpassword = request.form.get('cpwd')
        print(username, email, cpassword, password)

        if password == cpassword and len(username) > 2 and len(password) >= 6 and '@' in email and '.com' in email and len(email)>= 11:
            register = db.add_user(username, email, password)

            return redirect(url_for('login', data=errors))
        else:
            errors = "invalid details"

    return render_template('register.html', errors=errors)





# About
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
