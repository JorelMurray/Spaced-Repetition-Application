from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.project import Project
from flask_app.models.item import Item
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/additem')
def addItem():

    return render_template("index.html")

@app.route('/createitem', methods = ['POST'])
def createItem():

    return render_template("index.html")
    
@app.route('/edititem')
def editItem():
    pass

    return render_template("index.html")

@app.route('/updateitem', methods = ['POST'])
def updateItem():
    pass

    return render_template("index.html")

@app.route('/reviewitem')
def reviewItem():
    pass

    return render_template("index.html")


@app.route('/deleteitem')
def deleteItem():
    pass

    return redirect("dashboard.html")

