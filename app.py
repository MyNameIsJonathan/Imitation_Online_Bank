from flask import Flask
from flask_pymongo import PyMongo

# Create flask application
app = Flask(__name__)

# Configure flask app with link to mongodb using flask-pymongo. 
app.config["MONGO_URI"] = "mongodb://mongodb:27017/test"

# Expose database as the db attribute.
mongo = PyMongo(app)



@app.route("/")
def hello():
    my_person = mongo.db.people.find_one_or_404()
    return my_person['first']