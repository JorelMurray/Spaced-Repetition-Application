from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():

    return render_template("index.html")


@app.route('/login', methods = ["POST"])
def login():
    isValid = User.validate(request.form, 'Login')

    if not isValid:
        return redirect('/')

    data = { "email" : request.form["loginEmail"] }
    user_in_db = User.get_by_email(data)
    
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['loginPassword']):
        # if we get False after checking the password
        flash("Invalid Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['userId'] = user_in_db.id
    session['firstName'] = user_in_db.first_name
    session['lastName'] = user_in_db.last_name
    session['email'] = user_in_db.email


    return redirect ('/dashboard')


@app.route('/register', methods = ['POST'])
def register():

    isValid = User.validate(request.form, 'Registration')

    if not isValid:
        return redirect('/')

    print('passed validation')
    data = {
        'firstName' : request.form['fname'],
        'lastName' : request.form['lname'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
    }

    session['userId'] = User.addUser(data)
    session['firstName'] = request.form['fname']
    session['lastName'] = request.form['lname']
    session['email'] = request.form['email']

    print('created user and added to session')

    return redirect ('/dashboard')


@app.route('/logout')
def logout():
    session.clear()

    return redirect('/')

