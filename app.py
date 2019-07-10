from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
import synapsepy

# Create flask application
app = Flask(__name__)

# Configure flask app with link to mongodb using flask-pymongo. 
app.config["MONGO_URI"] = "mongodb://mongodb:27017/test"

# Expose database as the db attribute.
mongo = PyMongo(app)

# Initialize the Synapse Client
client = synapsepy.Client(
    client_id='client_id_rocahO4wHBiIdP8J0nVYqSyMmjlkutWv7XsZbFTx',
    client_secret='client_secret_YhSGjyRZdQgtpiAa9nsWXMN6oE05u2f7kqFc0lD8',
    fingerprint='static_pin',
    ip_address='1.2.3.132',
    devmode=True
)



@app.route("/")
def index():
    return render_template('index.html')

# TODO -- Make this POST to synapse to create an account
@app.route("/create_account", methods=["POST"])
def create_account():

    # Collect values from form
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phoneNumber = request.form['tel']
    birth_date = request.form['birth_date']
    street_address = request.form['street_address']
    city = request.form['city']
    state = request.form['state']
    postal_code = request.form['postal_code']
    country_code = request.form['country_code']
    ssn = request.form['ssn']
    govtid = request.form['govtid']

    # Artificially attribute IP, fingerprint. Fill in body with form values
    ip = '1.2.3.132'
    fingerprint = 'static_pin'
    body = {
        "logins": [
            {
                "email": "jonathanholson@gmail.com"
            }
        ],
        "phone_numbers": [
            "901.111.1111",
            "jonathanholson@gmail.com"
        ],
        "legal_names": [
            first_name + ' ' + last_name
        ],
        "documents": [{
            "email":email,
            "phone_number":phoneNumber,
            "ip":"::1",
            "name":first_name + ' ' + last_name,
            "alias":"Test",
            "entity_type":"M",
            "entity_scope":"Arts & Entertainment",
            "day":2,
            "month":5,
            "year":1989,
            "address_street":street_address,
            "address_city":city,
            "address_subdivision":state,
            "address_postal_code":postal_code,
            "address_country_code":country_code,
            "desired_scope": "SEND|RECEIVE|TIER|1",
            "doc_option_key": "INVESTOR_DOCS",
            "docs_key": "GOVT_ID_ONLY",
            "virtual_docs":[{
                "document_value":ssn,
                "document_type":"SSN"
            }],
            "physical_docs":[{
                "document_value": govtid,
                "document_type": "GOVT_ID"
            }],
            "social_docs":[{
                "document_value":"https://www.facebook.com/valid",
                "document_type":"FACEBOOK"
            }]
        }]
    }

    # Create user account
    client.create_user(body, ip, fingerprint=fingerprint)

    return redirect(url_for('new_account'))

@app.route("/new_account")
def new_account():
    my_person = mongo.db.people.find_one_or_404()
    return render_template('new_account.html', person=my_person['first'])

