from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

# added for email pattern validation
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



# ? --------------------------------------
    # READ all users, display on frontend
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL("users_schema").query_db(query)

        users = []

        for user in results:
            users.append(cls(user))
        
        return users
# ? --------------------------------------



# ? --------------------------------------
    # CREATE new user, add form data to database
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fname)s, %(lname)s, %(email)s, NOW(), NOW());"

        return connectToMySQL("users_schema").query_db(query, data)
# ? --------------------------------------



# ? --------------------------------------
    # READ one user, show on frontend
    @classmethod
    def get_one(cls, data):
        query  = "SELECT * FROM users WHERE id = %(id)s;" # * id, matching the table column
        result = connectToMySQL('users_schema').query_db(query, data)

        return cls(result[0]) # ! is this making an object out of the first result from the database? I think it is.
# ? --------------------------------------



# ? --------------------------------------
    # UPDATE user with form data
    @classmethod
    def update_one(cls, data):
        query  = "UPDATE users SET first_name = %(fname)s, last_name = %(lname)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s;" # * id, matching the table column

        return connectToMySQL('users_schema').query_db(query, data)
# ? --------------------------------------



# ? --------------------------------------
    # DELETE user
    @classmethod
    def remove_one(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"

        return connectToMySQL('users_schema').query_db(query, data)
# ? --------------------------------------



# ? --------------------------------------
    # valadate input fields
    @staticmethod
    def validate_form(data):
        is_valid = True # we assume this is true

        if len(data['fname']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(data['lname']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if len(data['email']) < 5:
            flash("Email must be at least 5 characters")
            is_valid = False

        return is_valid
# ? --------------------------------------



# ? --------------------------------------
    # valadate email pattern 
    @staticmethod
    def validate_email(data):
        is_valid = True

        # if pattern doesn't match flash message
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False

        return is_valid
# ? --------------------------------------