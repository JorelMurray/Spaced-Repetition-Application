# import the function that will return an instance of a connection
from mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import project
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Item:
    db = 'soloproject'

    def __init__( self , data ):
        self.id = data['id']
        self.itemName = data['itemName']
        self.category = data['category']
        self.masteryLevel = data['masteryLevel']
        self.status = data['status']
        self.attempts = data['attempts']
        self.createdDate = data['createdDate']
        self.updatedDate = data['updatedDate']
        self.projectId = data['projectId']

    
    @classmethod
    def addItem(cls, data ):
        query = "INSERT INTO items ( first_name , last_name , email , password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s, NOW() , NOW());"
        
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db).query_db( query, data )
    
    @classmethod
    def getOne(cls,data):
        query = "SELECT * FROM items WHERE Email = %(id)s;"
        result = connectToMySQL(Item.db).query_db(query,data)

        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate(item, formType):
        is_valid = True # we assume this is true

        if formType == "Login":

            query = 'SELECT * FROM USERS WHERE email = %(loginEmail)s;'
            result = connectToMySQL(User.db).query_db(query, user)
            print(len(result))
            if not EMAIL_REGEX.match(user['loginEmail']):
                flash("Must enter a valid loginemail address")
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
    def userRecipes(cls,data):
        query = "select * from users left join recipes on users.id = recipes.User_id WHERE users.id = %(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        user = cls(result[0])
        for row in result:
            data = {
                "id" : row['recipes.id'],
                "name" : row['name'],
                "description" : row['description'],
                "instructions" : row['instructions'],
                "date_made_on" : row['date_made_on'],
                "under_30_min" : row['under_30_min'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at'],
                "user_id" : row['User_id']
            }
            temp = recipe.Recipe(data)
            user.recipes.append(temp)
        return user

    @classmethod
    def deleteItem(cls, data ):
        query = "DELETE FROM users where id = %(id)s;"
        
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db).query_db( query, data )

    @classmethod
    def allItems(cls):
        query = "SELECT * FROM users"
        result = connectToMySQL(Item.db).query_db(query)

        allitems = []

        for r in result:
            allitems.append(r)

        return allitems

    @classmethod
    def getItemHistory(cls):
        pass


