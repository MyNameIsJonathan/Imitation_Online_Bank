from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import synapsepy
import datetime

import sys # TODO REMOVE
# print(f'my string', file=sys.stderr) # TODO REMOVE

# Create flask application
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Configure flask app with link to mongodb using flask-pymongo. 
app.config["MONGO_URI"] = "mongodb://mongodb:27017/flaskSite"

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

#Initialize our method for encrypting our submitted passwords
bcrypt = Bcrypt()
bcrypt.init_app(app)



@app.route("/")
def index():
    if "name" in session:
        return render_template('index.html', name=session['name'])
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":

        # Look for account associated with provided email
        user = mongo.db.users.find_one({"email" : request.form["email"]})

        # If user is found, make sure password matches. Login.
        if user:
            if bcrypt.check_password_hash(user['password'], request.form['password']):
                # login_user(user)
                session['email'] = request.form['email']
                session['name'] = user['first_name'] + ' ' + user['last_name']
                session['id'] = user['synapse_id']
                return redirect(url_for('account'))

            # If incorrect password
            flash('Invalid email/password combination. Please try again', 'danger')
            return redirect(url_for('login'))

        # If no user found, ask to register
        flash('No account found associated with the provided email. Please register', 'danger')
        return redirect(url_for('register'))

    # If method is "GET", render login page
    return render_template('login.html')


@app.route("/logout")
def logout():
    session['email'] = None
    session['name'] = None
    session['id'] = None
    return redirect(url_for('index'))


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # Look to see if account already exists for provided email
        user = mongo.db.users.find_one({'email' : request.form['email']}) 

        # If user is not found, create an account
        if user is None:

            # Confirm password and confirmation password are identical
            if request.form['password'] != request.form['password_conf']:
                flash('Passwords don\'t match! Please try again', 'danger')
                return redirect(url_for('register'))

            # Create hashes for encoded entries
            hashPass = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            hashPassConf = bcrypt.generate_password_hash(request.form['password_conf']).decode('utf-8')
            hashSSN = bcrypt.generate_password_hash(request.form['ssn']).decode('utf-8')
            hashGovtID = bcrypt.generate_password_hash(request.form['govtid']).decode('utf-8')

            # Convert date to datetime.date; get individual values
            birth_date = datetime.datetime.strptime(request.form['birth_date'], '%Y-%m-%d').date()

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
                    request.form['first_name'] + ' ' + request.form['last_name']
                ],
                "documents": [{
                    "email":request.form["email"],
                    "phone_number":request.form['phone_number'],
                    "ip":ip,
                    "name":request.form['first_name'] + ' ' + request.form['last_name'],
                    "alias":"Test",
                    "entity_type":"M",
                    "entity_scope":"Arts & Entertainment",
                    "day":birth_date.day,
                    "month":birth_date.month,
                    "year":birth_date.year,
                    "address_street":request.form['street_address'],
                    "address_city":request.form['city'],
                    "address_subdivision":request.form['state'],
                    "address_postal_code":request.form['postal_code'],
                    "address_country_code":request.form['country_code'],
                    "desired_scope": "SEND|RECEIVE|TIER|1",
                    "doc_option_key": "INVESTOR_DOCS",
                    "docs_key": "GOVT_ID_ONLY",
                    "virtual_docs":[{
                        "document_value":request.form['ssn'],
                        "document_type":"SSN"
                    }],
                    "physical_docs":[{
                        "document_value": request.form['govtid'],
                        "document_type": "GOVT_ID"
                    }],
                    "social_docs":[{
                        "document_value":"https://www.facebook.com/valid",
                        "document_type":"FACEBOOK"
                    }]
                }]
            }

            # Create user account
            new_user = client.create_user(body, ip, fingerprint=fingerprint)

            # Save user in MongoDB
            mongo.db.users.insert({
                'synapse_id':new_user.id,
                'email': request.form['email'],
                'password': hashPass,
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'phone_number': request.form['phone_number'],
                'birth_date': request.form['birth_date'],
                'street_address': request.form['street_address'],
                'city': request.form['city'],
                'state': request.form['state'],
                'postal_code': request.form['postal_code'],
                'country_code': request.form['country_code'],
                'ssn': hashSSN,
                'govtid': hashGovtID
            })

            # Report account creation successful, redirect
            flash('Account creation successful! Please login', 'success')
            return redirect(url_for('login'))

        # If user is found, flash the user and redirect to login
        flash('An account already exists with that email! Please login', 'danger')
        return redirect(url_for('login'))

    # If method is "GET", render register template
    return render_template('register.html')


@app.route("/account")
def account():
    # If user is logged in, render account page
    if "name" in session:
        return render_template('account.html', name=session['name'])

    # If user is not logged in, have them log in
    flash('Please login first!')
    return redirect(url_for('login'))


@app.route("/account_values", methods=["GET"])
def account_values():
    # If user is not logged in, have them log in
    if not "name" in session:
        flash('Please login first!')
        return redirect(url_for('login'))

    # Get user instance from Synapse
    user = client.get_user(session['id'], full_dehydrate=True)

    # Grab values to report
    values = {
        "name": user.body["documents"][0]["name"],
        "email": user.body["documents"][0]["email"],
        "phone_number": user.body["documents"][0][
            "phone_number"
        ],
        "birth_date": str(user.body["documents"][0]["month"])
        + "/"
        + str(user.body["documents"][0]["day"])
        + "/"
        + str(user.body["documents"][0]["year"]),
        "address_street": user.body['documents'][0]['address_street'],
        "address_city": user.body['documents'][0]['address_city'],
        "address_subdivision": user.body['documents'][0]['address_subdivision'],
        "address_postal_code": user.body['documents'][0]['address_postal_code'],
        "address_country_code": user.body['documents'][0]['address_country_code'],
    }
    
    return render_template('account_values.html', 
                           first_name=session['name'].split()[0], 
                           values=values)


@app.route("/update_account", methods=["GET", "POST"])
def update_account():
    # If user is not logged in, have them log in
    if not "name" in session:
        flash('Please login first!')
        return redirect(url_for('login'))

    # Get current user's id and synapse User account
    user_synapse_id = session['id']
    user = client.get_user(user_synapse_id, full_dehydrate=True)

    # If method is GET, pre-fill current account values in update form
    if request.method == "GET":

        # Render update_account
        return render_template(
            'update_account.html', name=session['name'])

    # If method is POST, update account with form information
    ip = '1.2.3.132'
    fingerprint = 'static_pin'

    # Instantiate the body dict, to hold value to update
    body = {'documents': []}

    # Select the item chosen to update, add to body; may be in two key-value pairs
    choice = request.form['update_choice']

    if choice == 'email':
        body['documents'] = [{'email':request.form['update_value']}]
        body['logins'] = [{'email': request.form['email']}]
    elif choice == 'name':
        body['documents'] = [{'name':request.form['update_value']}]
        body['legal_names'] = [request.form['update_value']]
    elif choice == 'phone_number':
        body['documents'] = [{'phone_number':request.form['update_value']}]
        body["phone_numbers"] = [request.form['phone_number']]
    elif choice == 'birth_date':
        pass
    elif choice == 'street_address':
        body['documents'] = [{'street_address':request.form['update_value']}]
    elif choice == 'city':
        body['documents'] = [{'city':request.form['update_value']}]
    elif choice == 'state':
        body['documents'] = [{'state':request.form['update_value']}]
    elif choice == 'postal_code':
        body['documents'] = [{'postal_code':request.form['update_value']}]
    elif choice == 'country_code':
        body['documents'] = [{'country_code':request.form['update_value']}]
    elif choice == 'ssn':
        body["virtual_docs"] = [{
                "document_value":request.form['ssn'],
                "document_type":"SSN"
        }]

    # Payload needs the following basic entities. Instantiate with current user values
    base_package = {
        'name': user.body['documents'][0]['name'],
        'email': user.body['documents'][0]['email'],
        'phone_number': user.body['documents'][0]['phone_number'],
        'entity_type': user.body['documents'][0]['entity_type'],
        'entity_scope': user.body['documents'][0]['entity_scope'],
        'ip': '1.2.3.132'
    }

    # Add base payload items to body payload
    for key, value in base_package.items():
        if key != choice:
            body['documents'][0][key] = value

    # Update account
    user.update_info(body)

    # Update session values
    if choice == 'email':
        session['email'] = request.form['update_value']
    elif choice == 'name':
        session['name'] = request.form['update_value']

    # Refresh Account to show updated values
    user = client.get_user(user.id)

    flash('Account updated successfully!', 'success')
    return redirect(url_for('update_account'))


@app.route("/open_deposit_account", methods=["GET", "POST"])
def open_deposit_account():
    # If user is not logged in, have them log in
    if not "name" in session:
        flash('Please login first!')
        return redirect(url_for('login'))

    # If method is GET, render html
    if request.method == "GET":
        return render_template('open_deposit_account.html')

    # Select the current user's synapse account
    user = client.get_user(session['id'])

    # Create body to hold deposit account information
    body = {
        "type": "DEPOSIT-US",
        "info": {
            "nickname": request.form['account_nickname'],
            "document_id": user.body['documents'][0]['id']
        }
    }

    # Open deposit account
    user.create_node(body, idempotency_key='123456')

    flash('Account created successfully!', 'success')
    return redirect(url_for('account'))


@app.route("/close_deposit_account", methods=["GET", "POST"])
def close_deposit_account():
    # If user is not logged in, have them log in
    if not 'name' in session:
        flash('Please login first!')
        return redirect(url_for('login'))

    # Get user account
    user = client.get_user(session['id'])

    # If method if GET
    if request.method == "GET":

        # Get deposit account(s)
        nodes = user.get_all_nodes().list_of_nodes
        desposit_accounts = [node for node in nodes if node.body['type'] == 'DEPOSIT-US']

        # Save account(s) in list of dicts
        accounts = [
            {'id': node.id, 'name': node.body['info']['nickname']}
            for node in desposit_accounts
        ]

        return render_template('close_deposit_account.html', accounts=accounts)
    
    # If method is POST, get the chosen account, set to inactive
    node = request.form['account_choice']
    node.body['is_active'] = False

    flash('Account successfully inactivate!', 'success')
    return redirect(url_for('account'))



@app.route("/view_savings", methods=["GET"])
def view_savings():
    pass



