from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# ? --------------------------------------
# READ all users, display on frontend
@app.route('/') 
def index():
    return render_template("read.html", users = User.get_all())  
# ? --------------------------------------



# ? --------------------------------------
# add new user form page
@app.route('/add/user') 
def add_user():
    return render_template("create.html")  

# CREATE new user, POST data
# @app.route('/create/user', methods=['POST']) 
# def create_user():

    # * updated to include the input validation
    # * if it's not valid, redirects back to the form page so you can see the flash messages
    # if not User.validate_form(request.form):
    #     return redirect("/add/user")

    # * updated to include email pattern validation
    # * if it's not valid, redirects back to the form page so you can see the flash messages
    # if not User.validate_email(request.form):
    #     return redirect("/add/user")

    # User.save(request.form)

    # return redirect('/') 
# ? --------------------------------------



# ? --------------------------------------
# CREATE new user, POST data
# // todo: combining all the validation into one method, update the above route to reflect that change
@app.route('/create/user', methods=['POST']) 
def create_user():

    if not User.registration(request.form):
        return redirect("/add/user")

    # * have to do it this way instead of just passing request.form in the save() method because we need to hash the password first
    data = {
        "password": bcrypt.generate_password_hash(request.form['password']),
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "email": request.form['email'],
    }

    User.save(data)

    # *this isn't necessary. Nice I guess, if you're registration isn't redirecting to the logged in page
    # flash("Thanks for registering")
    return redirect('/') 
# ? --------------------------------------



# ? --------------------------------------
# if this assignment had a login feature this is how it would work. No new method, still just selecting user by email
# ? this is how he did it in class. Different on the platform and from how I've been doing it
# @app.route('/login/user', methods=['POST']) 
# def login_user():
#     user = User.get_by_email(request.form['email_address'])

#     if not user or not bcrypt.check_password_hash(user.password, request.form['password']): # hashed password first, password to be checked
#         flash("Invalid Credentials", "login")
#         return redirect('/')

    # * redirect to whatever the login page is. I don't have a login page for this assignment
    # ! how do you stop someone from just typing in this url and going to the dashboard?
    # return redirect('/dashboard')

# ? this is how the platform is doing it
@app.route('/login/user', methods=['POST']) 
def login_user():
    data = { 
        "email" : request.form["email"] 
    }
    
    user = User.get_by_email(data)

    # * if user doesn't exist or passwords don't match
    # * hashed password first, password to be checked second
    if not user or not bcrypt.check_password_hash(user.password, request.form['password']): 
        flash("Invalid Credentials")
        return redirect('/')

    # ! where is this coming from? Is there an input somewhere with the name user_id?? What is it doing??
    session['user_id'] = user.id

    # * redirect to whatever the login page is. I don't have a login page for this assignment
    # ! how do you stop someone from just typing in this url and going to the dashboard?
    # return redirect('/dashboard')
# ? --------------------------------------



# ? --------------------------------------
# READ one user, show on frontend in filled-out form
@app.route('/update/user/<int:id>') 
def update_user(id):   
    data = { 
        "id": id # id key, matches the column in the database, the name of the hidden input in the form
    }

    return render_template("update.html", user = User.get_one(data))  

# UPDATE user, collect form data
# need hidden input on the form with the user id
@app.route('/update/user', methods=['POST']) 
def update_user_form():
    User.update_one(request.form)

    return redirect("/")  
# ? --------------------------------------



# ? --------------------------------------
# READ user, show on frontend
@app.route('/view/user/<int:id>') 
def view_user(id):
    data = { 
        "id": id # id, the column in the database
    }

    return render_template("view.html", user = User.get_one(data))  
# ? --------------------------------------



# ? --------------------------------------
# DELETE user
@app.route('/delete/user/<int:id>') 
def delete_user(id):

    data ={ 
        "id": id # id, the column in the database
    }

    User.remove_one(data)

    return redirect("/")  
# ? --------------------------------------
