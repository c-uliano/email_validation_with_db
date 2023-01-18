from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

# is this needed in the model file? Didn't include it here during the class example
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)

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
    # READ user by email address, method used within another method in this file, for email validation, to see if an email address has already been registered
    # ? this is how he did it in class. Different on the platform and from how I've been doing it
    # @classmethod
    # def get_by_email(cls, email):
    #     query  = "SELECT * FROM users WHERE email = %(email)s;"

    #     results = connectToMySQL('users_schema').query_db(query, {'email': email})

    #     return cls(results[0]) if results else None

    # ? this is how the platform is doing it
    @classmethod
    def get_by_email(cls, data):
        query  = "SELECT * FROM users WHERE email = %(email)s;"

        result = connectToMySQL('users_schema').query_db(query, data)

        # * if there's nothing in the database for this query
        if len(result) < 1:
            return False

        return cls(result[0]) if result else None
# ? --------------------------------------



# ? --------------------------------------
    # valadate input fields
    # @staticmethod
    # def validate_form(data):
    #     is_valid = True # we assume this is true

    #     if len(data['fname']) < 3:
    #         flash("First name must be at least 3 characters.")
    #         is_valid = False
    #     if len(data['lname']) < 3:
    #         flash("Last name must be at least 3 characters.")
    #         is_valid = False
    #     if len(data['email']) < 5:
    #         flash("Email must be at least 5 characters")
    #         is_valid = False

    #     return is_valid
# ? --------------------------------------



# ? --------------------------------------
    # valadate email pattern 
    # @staticmethod
    # def validate_email(data):
    #     is_valid = True

    #     # if pattern doesn't match flash message
    #     if not EMAIL_REGEX.match(data['email']): 
    #         flash("Invalid email address!")
    #         is_valid = False

    #     return is_valid
# ? --------------------------------------



# ? --------------------------------------
    # playing with combining all the validation into one methond
    # ! how to make the content already added in the form stay even when the flash messages appear??
    @staticmethod
    def registration(data):
        is_valid = True

        if len(data['fname']) == 0:
            flash("Please enter a first name.")
            is_valid = False

        if len(data['lname']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False

        # * probably don't really need this if you're doing the regex for the email
        # if len(data['email']) < 5:
        #     flash("Email must be at least 5 characters")
        #     is_valid = False

        # to check if an email address is already registered. Requires another classmethod, added above
        if User.get_by_email(data['email_address']):
            flash("Email already taken")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False

        # * if this had been a registration form this would be the validation for that
        # * for a password input and confirm password input
        # if len(data['password']) < 8:
        #     flash("Password must be at least 8 characters", "register")
        #     is_valid = False

        # if data['password'] != data['password_confirm']:
        #     flash("Passwords need to match","register")
        #     is_valid = False


        return is_valid
# ? --------------------------------------



# ? --------------------------------------
    # * if this has included a login page this is what would be used
    @staticmethod
    def login(data):
        pass
# ? --------------------------------------