# import the function that will return an instance of a connection
from mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import item
import re
import pandas as pd
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
#This is a git test
class Project:
    db = 'soloproject'

    def __init__( self , data ):
        self.id = data['id']
        self.projectName = data['projectName']
        self.description = data['description']
        self.createdDate = data['createdDate']
        self.updatedDate = data['updatedDate']
        self.userId = data['userId']
        self.items = [] 

    
    @classmethod
    def addProject(cls, f, data ):

        query = "INSERT INTO projects ( projectName , description , createdDate, updatedDate, userId ) VALUES ( %(projectName)s , %(description)s , NOW() , NOW(), %(userId)s);"
    
        pID = connectToMySQL(cls.db).query_db( query, data)

        if f.filename != '':
            item.Item.importItems(pID,f)

        return pID
    
    @classmethod
    def getOne(cls,data):
        query = "SELECT * FROM projects WHERE id = %(id)s;"
        result = connectToMySQL(Project.db).query_db(query,data)

        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate(project, formType):
        is_valid = True # we assume this is true

        if formType == "Login":

            query = 'SELECT * FROM USERS WHERE email = %(loginEmail)s;'
            result = connectToMySQL(Project.db).query_db(query, project)
            print(len(result))
            if not EMAIL_REGEX.match(project['loginEmail']):
                flash("Must enter a valid loginemail address")
                is_valid = False


            elif len(result) < 1:
                is_valid = False
                flash("The email entered is not currently registered.")
                


        elif formType == 'Registration':
        
            query = 'SELECT * FROM USERS WHERE email = %(email)s;'
            result = connectToMySQL(Project.db).query_db(query, project)

            if not EMAIL_REGEX.match(project['email']):
                flash("Must enter a valid email address")
                is_valid = False
                print(project['email'])

            if len(result) >= 1:
                is_valid = False
                flash("That email is already registered to a user.")

            if len(project['password']) < 3:
                is_valid = False
                flash('The password must be greater than 3 characters')

            if project['password'] != project['confirm']:
                is_valid = False
                flash('Your passwords entered must match.')


        return is_valid

    @classmethod
    def projectItems(cls,data):
        query = "select * from projects left join items on projects.id = items.projectId WHERE projects.id = %(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        project = cls(result[0])
        for row in result:
            data = {
                "id" : row['items.id'],
                "itemName" : row['itemName'],
                "category" : row['category'],
                "confidenceLevel" : row['confidenceLevel'],
                "difficultyLevel" : row['difficultyLevel'],
                "status" : row['status'],
                "attempts" : row['attempts'],
                "createdDate" : row['createdDate'],
                "updatedDate" : row['updatedDate'],
                "projectId" : row['projectId'] 
            }
            temp = item.Item(data)
            project.items.append(temp)
        return project

    @classmethod
    def deleteProject(cls, data ):
        query = "DELETE FROM projects where id = %(id)s;"

        item.Item.deleteProjectItems(data)

        
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db).query_db( query, data )

    @classmethod
    def userProjects(cls):
        query = "SELECT * FROM projects"
        result = connectToMySQL(Project.db).query_db(query)

        allprojects = []

        for r in result:
            allprojects.append(r)

        return allprojects



