# import the function that will return an instance of a connection
from cmath import nan
from mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import project
import re
import pandas as pd
import numpy as np
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Item:
    db = 'soloproject'

    def __init__( self , data ):
        self.id = data['id']
        self.itemName = data['itemName']
        self.category = data['category']
        self.confidenceLevel = data['confidenceLevel']
        self.difficultyLevel = data['difficultyLevel']
        self.status = data['status']
        self.attempts = data['attempts']
        self.createdDate = data['createdDate']
        self.updatedDate = data['updatedDate']
        self.projectId = data['projectId']
        self.itemURL = data['itemURL']


    @staticmethod
    def validate(form):

        is_valid = True # we assume this is true

        if len(form['itemName']) < 1:
            is_valid = False
            flash('You must enter an Item Name. ')
        if len(form['category']) < 1:
            is_valid = False
            flash('You must enter a Category. ')
        if form['difficultyLevel'] == "0":
            is_valid = False
            flash('You must enter a Difficulty. ')

        
        return is_valid

    @classmethod
    def addItem(cls, data ):

        query = "INSERT INTO items ( itemName , category , confidenceLevel, difficultyLevel , status, attempts, createdDate, updatedDate, projectId, itemURL ) VALUES ( %(itemName)s , %(category)s , 0, %(difficultyLevel)s, 'New', 0, NOW() , NOW(), %(pID)s, %(itemURL)s);"
        
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db).query_db( query, data )

    @classmethod
    def bookAttempt(cls, data ):

        query = "INSERT INTO attempt_history (attemptDate, projectName, itemName, category, confidenceLevel, difficultyLevel, status, attempts, items_id) SELECT NOW(), projects.projectName, itemName, category, confidenceLEvel, difficultyLevel, status, attempts, items.id from items join projects on projects.id = items.projectId where items.id = %(id)s;"
        
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db).query_db( query, data )
    
    @classmethod
    def getOne(cls,data):
        query = "SELECT * FROM items WHERE id = %(id)s;"
        result = connectToMySQL(Item.db).query_db(query,data)

        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def importItems(cls, pID, f):

        df = pd.read_excel(f)


        df['URL'] = df['URL'].fillna("")

        for ind in df.index:

            item = {    
                'itemName' : df['Item'][ind],
                'category' : df['Category'][ind],
                'difficultyLevel' : df['Difficulty'][ind],
                'itemURL' : df['URL'][ind],
                'projectId': pID
            }

            query = "INSERT INTO items ( itemName , category , confidenceLevel, difficultyLevel, status, attempts, createdDate, updatedDate, projectId, itemURL ) VALUES ( %(itemName)s , %(category)s , 0, %(difficultyLevel)s ,'New', 0, NOW() , NOW(), %(projectId)s, %(itemURL)s);"
            connectToMySQL(cls.db).query_db( query, item )
            
        return pID

    @classmethod
    def deleteItem(cls, data ):
        query = "DELETE FROM items where id = %(id)s;"

        Item.deleteItemHistory(data)
        
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db).query_db( query, data )

    @classmethod
    def deleteItemHistory(cls, data ):
        query = "DELETE FROM attempt_history where items_id = %(id)s;"
        
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db).query_db( query, data )

    @classmethod
    def deleteProjectItems(cls, data ):
        query = "DELETE FROM items where projectId = %(id)s;"
        
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db).query_db( query, data )

    @classmethod
    def updateItem(cls, data):

        query = "UPDATE items SET itemName = %(itemName)s, category = %(category)s, difficultyLevel = %(difficultyLevel)s, itemURL = %(itemURL)s WHERE id = %(id)s"

        return connectToMySQL(cls.db).query_db( query, data ) 

    @classmethod
    def attemptItem(cls, data):

        query = "UPDATE items SET status = 'In Progress' WHERE id = %(id)s"

        return connectToMySQL(cls.db).query_db( query, data ) 

    @classmethod
    def getOpenItemCount(cls, data):
        query = "SELECT COUNT(id) FROM items WHERE projectID = %(pID)s AND status = 'In Progress';"

        result = connectToMySQL(cls.db).query_db( query, data )

        return result[0]['COUNT(id)']

    @classmethod
    def reviewItem(cls, data):

        query = "UPDATE items SET status = 'Completed', attempts = attempts + 1, confidenceLevel = %(confidenceLevel)s WHERE id = %(id)s"
        
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


