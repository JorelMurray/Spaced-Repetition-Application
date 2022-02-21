from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.project import Project
from flask_app.models.item import Item
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/additem/<int:pID>')
def addItem(pID):
    if 'userId' not in session:
        flash('Please log in')
        return redirect('/')    

    return render_template("newitem.html", pID = pID)

@app.route('/createitem', methods = ['POST'])
def createItem():
    if 'userId' not in session:
        flash('Please log in')
        return redirect('/')

    data = {
        "itemName" : request.form['itemName'],
        "category" : request.form['category'],
        "pID" : request.form['pID']
    }

    Item.addItem(data)

    return redirect(f"/viewproject/{request.form['pID']}/")

@app.route('/importitems', methods = ['POST'])
def importItems():
    if 'userId' not in session:
        flash('Please log in')
        return redirect('/')

    f = request.files['file']

    pID = request.form['pID']

    if f.filename != '':
        pID = Item.importItems(request.form['pID'], f)

    print("proeceed")

    return redirect (f"/viewproject/{pID}/")
    
@app.route('/edititem/<int:pID>/<int:itemID>/')
def editItem(pID, itemID):
    if 'userId' not in session:
        flash('Please log in')
        return redirect('/')

    data = {
        "id" : itemID
    }

    return render_template("edititem.html", currentItem = Item.getOne(data), pID = pID)

@app.route('/updateitem', methods = ['POST'])
def updateItem():
    if 'userId' not in session:
        flash('Please log in')
        return redirect('/')

    data = {
        "id" : request.form['itemID'],
        "itemName" : request.form['itemName'],
        "category" : request.form['category']
    }

    Item.updateItem(data)

    return redirect(f"/viewproject/{request.form['pID']}/")

@app.route('/reviewitem/<int:itemID>')
def reviewItem(itemID):
    pass

    return render_template("index.html")

@app.route('/attemptitem/<int:itemID>')
def attemptItem(itemID):
    pass

    return render_template("index.html")

@app.route('/deleteitem/<int:pID>/<int:itemID>')
def deleteItem(pID, itemID):
    data = {
        'id': itemID
    }
    Item.deleteItem(data)

    return redirect(f"/viewproject/{pID}/")

