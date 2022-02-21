# import the function that will return an instance of a connection
from mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import project
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db = 'soloproject'

    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['firstName']
        self.last_name = data['lastName']
        self.email = data['email']
        self.password = data['password']
        self.createdDate = data['createdDate']
        self.updatedDate = data['updatedDate']
        self.projects = []

    
    @classmethod
    def addUser(cls, data ):
        query = "INSERT INTO users ( firstName , lastName , email , password, createdDate, updatedDate ) VALUES ( %(firstName)s , %(lastName)s , %(email)s , %(password)s, NOW() , NOW());"
        
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db).query_db( query, data )
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(User.db).query_db(query,data)

        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def getOne(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(User.db).query_db(query,data)

        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate(user, formType):
        is_valid = True # we assume this is true

        if formType == "Login":

            query = 'SELECT * FROM USERS WHERE email = %(loginEmail)s;'
            result = connectToMySQL(User.db).query_db(query, user)
            print(len(result))
            if not EMAIL_REGEX.match(user['loginEmail']):
                flash("Must enter a valid email address")
                is_valid = False


            elif len(result) < 1:
                is_valid = False
                flash("The email entered is not currently registered.")
                


        elif formType == 'Registration':
        
            query = 'SELECT * FROM USERS WHERE email = %(email)s;'
            result = connectToMySQL(User.db).query_db(query, user)

            if not EMAIL_REGEX.match(user['email']):
                flash("Must enter a valid email address")
                is_valid = False
                print(user['email'])

            if len(result) >= 1:
                is_valid = False
                flash("That email is already registered to a user.")

            if len(user['password']) < 3:
                is_valid = False
                flash('The password must be greater than 3 characters')

            if user['password'] != user['confirm']:
                is_valid = False
                flash('Your passwords entered must match.')


        return is_valid

    @classmethod
    def userProjects(cls,data):
        query = "select * from users left join projects on users.id = projects.userId WHERE users.id = %(id)s order by projectName desc"
        result = connectToMySQL(cls.db).query_db(query, data)
        user = cls(result[0])
        print(user)
        for row in result:
            data = {
                "id" : row['projects.id'],
                "projectName" : row['projectName'],
                "description" : row['description'],
                "createdDate" : row['createdDate'],
                "updatedDate" : row['updatedDate'],
                "userId" : row['userId']

            }
            temp = project.Project(data)
            user.projects.append(temp)
            print(user.projects)
        return user

    @classmethod
    def deleteUser(cls, data ):
        query = "DELETE FROM users where id = %(id)s;"
        
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db).query_db( query, data )

    @classmethod
    def allUsers(cls):
        query = "SELECT * FROM users"
        result = connectToMySQL(User.db).query_db(query)

        allusers = []

        for r in result:
            allusers.append(r)

        return allusers



