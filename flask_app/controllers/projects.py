from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_app.models.user import User
from flask_app.models.project import Project
from flask_app.models.item import Item
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

confidenceRef = {
    0 : "New",
    1 : "Very Low",
    2 : "Low",
    3 : "Medium",
    4 : "High",
    5 : "Very High"
}
difficultyRef = {
    1 : "Very Easy",
    2 : "Easy",
    3 : "Medium",
    4 : "Hard",
    5 : "Very Hard"
}

@app.route('/dashboard') 
def dashboard():
    if 'userId' not in session:
        flash('Please log in')
        return redirect('/')
    else:
        data = {
            'id': session['userId'] 
        }

    return render_template("dashboard.html", projectList = User.userProjects(data))

@app.route('/viewproject/<int:pID>/')
def viewproject(pID):
    if 'userId' not in session:
        flash('Please log in')
        return redirect('/')
    else:
        data = {
            'id': pID
        }

    return render_template("viewproject.html", currentProject = Project.getOne(data), itemList = Project.projectItems(data), confidenceRef = confidenceRef, difficultyRef = difficultyRef)


@app.route('/newproject')
def newproject():
    if 'userId' not in session:
        flash('Please log in')
        return redirect('/')

    return render_template("newproject.html")

@app.route('/createproject', methods = ['POST'])
def upload_file():
    if 'userId' not in session:
        flash('Please log in')
        return redirect('/')
    
    isValid = Project.validate(request.form)

    if not isValid:
        return redirect("/newproject")
    
    data = {
        'userId': session['userId'], 
        'projectName' : request.form['projectName'],
        'description' : request.form['description']
    }
    f = request.files['file']

    pID = Project.addProject(f, data)

    return redirect (f"/viewproject/{pID}/")

@app.route('/projectanalytics')
def projectAnalytics():
    pass

    return render_template("index.html")


@app.route('/deleteproject/<int:pID>/')
def deleteProject(pID):
    data = {
            'id': pID
        }
    Project.deleteProject(data)

    return redirect("/dashboard")


@app.route('/user/<int:userId>/')
def viewUserProjects(userId):
    if 'userId' not in session:
        flash('Please log in')
        return redirect('/')
    
    data = {
            'id': userId
    }
    myprojects = User.userProjects(data)
    return render_template('viewUserProjects.html', projectList = myprojects)

@app.route('/spacedrepetition/<int:pID>')
def spacedRepetition(pID):
    if 'userId' not in session:
        flash('Please log in')
        return redirect('/')
    
    data = {
            'id': pID,
            'pID' : pID
    }

    return render_template('spacedrepetition.html', currentProject = Project.getOne(data), itemList = Project.projectItems(data), availableItems = 3 - Item.getOpenItemCount(data) )

@app.route('/generateitems', methods = ['POST'])
def generateItems():

    data = {
        "pID" : request.form['pID'],
        "itemCount" : request.form['itemCount']
    }

    openItems = Item.getOpenItemCount(data)

    if request.form['itemCount'] == "0":
        flash("Please select an item count")
        return redirect (f"spacedrepetition/{data['pID']}")

    elif openItems + int(data['itemCount']) > 3:
        flash("You can only have 3 items in progress at a time.")
        return redirect (f"spacedrepetition/{data['pID']}")

    generatedItems = Project.generateItems(data)

    flash(f"Generated {len(generatedItems.items)} item(s)!")

    return redirect (f"/viewproject/{request.form['pID']}/")
