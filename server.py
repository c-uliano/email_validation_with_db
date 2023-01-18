from flask_app import app
from flask_app.controllers import users
# all your controller files need to be imported here, or the routes won't work

if __name__=="__main__": 
    app.run(debug=True) 

