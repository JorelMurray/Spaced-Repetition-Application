from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_app.models.user import User
from flask_app.models.project import Project
from flask_app.models.item import Item
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


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

    return render_template("viewproject.html", currentProject = Project.getOne(data), itemList = Project.projectItems(data))


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
    
    data = {
        'userId': session['userId'], 
        'projectName' : request.form['name'],
        'description' : request.form['description']
    }
    f = request.files['file']

    pID = Project.addProject(f, data)

    return redirect (f"/viewproject/{pID}/")

@app.route('/projectanalytics')
def projectAnalytics():
    pass

    return render_template("index.html")

@app.route('/spacedrepetition')
def spacedRepetition():
    pass

    return render_template("index.html")

@app.route('/deleteproject/<int:pID>/')
def deleteProject(pID):
    data = {
            'id': pID
        }
    Project.deleteProject(data)

    return redirect("dashboard.html")


@app.route('/user/<int:userId>/')
def viewUserProjects(userId):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    
    data = {
            'id': userId
    }
    myprojects = User.userProjects(data)
    return render_template('viewUserProjects.html', projectList = myprojects)
