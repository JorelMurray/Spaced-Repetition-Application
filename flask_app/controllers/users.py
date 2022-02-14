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
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    session['last_name'] = user_in_db.last_name
    session['email'] = user_in_db.email


    return redirect ('/dashboard')


@app.route('/register', methods = ['POST'])
def register():

    isValid = User.validate(request.form, 'Registration')

    if not isValid:
        return redirect('/')


    data = {
        'first_name' : request.form['fname'],
        'last_name' : request.form['lname'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
    }

    session['user_id'] = User.addUser(data)
    session['first_name'] = request.form['fname']
    session['last_name'] = request.form['lname']
    session['email'] = request.form['email']

    return redirect ('/dashboard')


@app.route('/logout')
def logout():
    session.clear()

    return redirect('/')

@app.route('/user/<int:user_id>/')
def viewUserProjects(user_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    else:
        data = {
            'id': user_id
        }
        myprojects = User.userProjects(data)
        return render_template('viewUserProjects.html', projectList = myprojects)
