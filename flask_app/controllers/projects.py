from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
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


    return render_template("dashboard.html", allProjects = User.userProjects(data))

@app.route('/viewproject/<int:projectId>/')
def viewproject():
    pass

    return render_template("index.html")

@app.route('/newproject')
def newproject():
    pass

    return render_template("index.html")

@app.route('/createproject', methods = ['POST'])
def createProject():
    pass

    return render_template("index.html")

@app.route('/projectanalytics')
def projectAnalytics():
    pass

    return render_template("index.html")

@app.route('/spacedrepetition')
def spacedRepetition():
    pass

    return render_template("index.html")

@app.route('/deleteproject')
def deleteProject():
    pass

    return redirect("dashboard.html")



@app.route('/user/<int:userId>/')
def viewUserProjects(userId):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    else:
        data = {
            'id': userId
        }
        myprojects = User.userProjects(data)
        return render_template('viewUserProjects.html', projectList = myprojects)
