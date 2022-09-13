'''
Programe Name: User Keystokre Dynamics Detection using Machine Learning
Supervisor: Andrew Stratton
Purpose: Dissertation Thesis
Organisation: University of Sheffield
Developer: Kunal Das
'''
'''Add Liabries'''
from copyreg import pickle
from datetime import timedelta
from email import message
import calendar
import time
from datetime import datetime
from flask_session import Session
import config
import re
import os
from os import environ, path
import pymongo
import json
from flask import Flask, redirect, url_for, render_template, request, flash, session, jsonify, g
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from bson import json_util, ObjectId
import json
import uuid
import pickle
from model import Validation
from cryptography.hazmat.primitives.asymmetric import ec

# MongoDB connection URL
uri = 'mongodb+srv://continuesauth.gqcdh.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&ssl=true'

# Creating Flask App
app = Flask(__name__)
#app.config['SECRET_KEY'] = os.urandom(24)
app.config['SECRET_KEY'] = 'h\xd0Pp\x17\xe0ZG\xfe\xa9\xa9\xf1\xe6\xb9\xc1\xedQ\xf1\xcdO=\x00\x01\xd6[\xff\x88k\xae\xfd\xa6\x9c' # Create Secrect Key which is encrypted
app.config['SESSION_COOKIE_NAME'] = "Authentication_Session" # Set Session Name
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True) # Setting for Cookie
app.config['PERMANENT_SESSION'] = True # Set Session on 

bcrypt = Bcrypt(app) # Set Password hasing to app

# Adding MongoDB token key from file which is valid for 2 years
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='static/certificate/X509-cert-666372965419332429.pem')

db = client['dissertation'] # Select Database
# Select Collection
userCollection = db['users'] 
keyCollection = db['keystrock_dynamics']
mouseCollection = db['mouse_dynamics']
sessionCollection = db['session']
 
# Validator for keystroke time intervals
behaviour = 0
validator = 0
biometricTemp = []

# Validator for mouse dynamics time intervals
mouseBehaviour = 0
mouseValidator = 0
mouseBiometricTemp = []

@app.route('/')
def index():
    sessionKey = session.get('session_key') # Selecting Session Key
    print(f'Session Index Key:{sessionKey}')
    # If session key is avaialble then select home page or back to login page
    if sessionKey == None:
        return render_template('index.html')
    else:
        print('Session',session.get('session_key'))
        return redirect(url_for('dashboard'))

@app.route('/registration')
def registration():
    sessionKey = session.get('session_key') # Selecting Session Key
    print(f'Session Registration Key:{sessionKey}')
    # If session key is avaialble then select home page or back to login page
    if sessionKey == None:
        return render_template('registration_form.html')
    else:
        return redirect(url_for('dashboard'))


@app.route('/security', methods=['POST', 'GET'])
def authentication():
    if request.method == 'POST':
        userEmail = request.form['user_email'] # Stroing email from html form submission
        userPassword = request.form['user_pwd'] # Stroing password from html form submission

        inputEmail = re.match(r'^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$', userEmail) # Check input type is email or not for an extra lyer of security
        if bool(inputEmail) == True:
            userEmail = userEmail.lower() # set email words to lower 

        myquery = {'email': userEmail} # set query for MongoDb
        checkUser = userCollection.count_documents(myquery); # Document Count from a single user email
        
        # Checking if user is avialable or not
        if checkUser > 0:
            userData = userCollection.find(myquery) # Executing query to get data from the user
            dbPassword = userData[0]['password'] # Get user password from database
            dbUserId = userData[0]['_id'] # Get User Id
            dbUserName = userData[0]['fullName'] # Get user password
            dbUserId = json.loads(json_util.dumps(dbUserId))['$oid'] # Remove user id object and convert into string
            print(dbUserName)
            hasedUserPassword = bcrypt.generate_password_hash(userPassword) # Encrypt current password
            checkPassword = bcrypt.check_password_hash(dbPassword, userPassword) # Check current password and will retunr true or fasle
            
            # Check if passwor is true or false
            if checkPassword == True:
                server_private_key = ec.generate_private_key(ec.SECP256K1()) # Generate private key for server
                private_key = ec.generate_private_key(ec.SECP256K1()) # Generate another private key
                shared_key = server_private_key.exchange(ec.ECDH(), private_key.public_key()) # Generate shared key

                session['session_key'] = shared_key # Create a dynaic session for secure connection
                session['profile'] = {"userId": dbUserId, "userName": dbUserName} # Create session value
                gmt = time.gmtime() # Get current time 
                timeStamp = calendar.timegm(gmt) # Get current timestamp
                dataTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Get current date and time
                # Recording session entry time for every user
                sessionEntry = sessionCollection.insert_one({'sessionKey':session.get('session_key'), 'name': session.get('profile')['userName'], 'userId': session.get('profile')['userId'], 'datetime':dataTime, 'timestamp': timeStamp})
                return redirect(url_for('dashboard')) # If successfull retunr to dashboard
            else:
                session.clear() # Clear the session
                alert = [{"type":"warning","name":"Invalid","description":"Username or Password!"}] # Message for error or warning
                return render_template('index.html', alert=alert)
        else:
            session.clear()
            alert = [{"type":"danger","name":"Error","description":"User Doesn't Exist."}] # Message for error or warning
            return render_template('index.html', alert=alert)

@app.route('/submit-details', methods=['POST', 'GET'])
def user_registration():
    if request.method == 'POST':
        firstName = Validate.valText(request.form['first_name']) # get user first name
        middleName = Validate.valText(request.form['middle_name']) # get user middile name
        lastName = Validate.valText(request.form['last_name']) # get user last name
        fullName = combine(firstName,middleName,lastName) # Create full name for future use
        email = Validate.valEmail(request.form['email']) # Getting user email
        email = email.lower() # Lowering the email 
        checkEmail = {'email': email} # Create query for MongoDB
        checkUser = userCollection.count_documents(checkEmail); # Run query for that email
        # Check if user is available or not
        if checkUser > 0:
            alert = [{"type":"warning","name":"Warning","description":"User Already Exist."}] # Set warning
            return render_template('registration_form.html', alert=alert) # If user already exist
        password = bcrypt.generate_password_hash(request.form['pwd']) # Encrypting password
        #Inserting User Data
        entry = userCollection.insert_one(
            {'fullName':fullName, 'firstName': firstName, 'middleName': middleName, 'lastName': lastName, 'email': email, 'password': password})
        return redirect(url_for('index')) #Successfull entry goes to login page

@app.route('/read')
def read():
    sessionKey = session.get('session_key') # Selecting Session Key
    print(f'Session Read Key:{sessionKey}')
    # If session key is avaialble then select home page or back to login page
    if sessionKey == None:
        session.clear()
        custMessage = 'Sorry! Session Out';
        return render_template('logout.html', message=custMessage)
    else:
        return render_template('read.html')

@app.route('/dashboard')
def dashboard():
    sessionKey = session.get('session_key') # Selecting Session Key
    print(f'Session Dashboard Key:{sessionKey}')
    # If session key is avaialble then select home page or back to login page
    if sessionKey == None:
        session.clear()
        custMessage = 'Sorry! Session Out';
        return render_template('logout.html', message=custMessage)
    else:
        return render_template('dashboard.html')

@app.route('/mouseauth', methods=['GET','POST'])
def mouseauth():
    global mouseBehaviour
    global mouseValidator
    global mouseBiometricTemp
    if request.method == "POST":
        sessionKey = session.get('session_key') # Selecting Session Key
        if sessionKey == None:
            return jsonify({'status': 'fail'}) # Return fail if session out
        else:
            #modelVal = Validation('1','Started')
            sessionUser = session.get('profile')['userId'] # Select user id from session
            data= request.get_json()
            data['user'] = session.get('profile')['userId'] # Select user id from session
            structure = json.loads(str(json.dumps(data))) # Create json stucture with user id
             # Check if current behaviour goes more than 18 or not
            if mouseBehaviour >= 100:
                # Check if suspicious behaviour goes more than 18 or not
                if len(mouseBiometricTemp) >= 18:
                    return jsonify({'status': 'success'})
                else:
                    mouseBiometricTemp.append(structure)
                    print(mouseBiometricTemp)
                    return jsonify({'status': 'continue'})
            else:
                mouseBehaviour += 1
                mouseCollection.insert_one(structure)
                return jsonify({'status': 'continue'})

@app.route('/auth', methods=['GET','POST'])
def auth():
    global behaviour
    global validator
    global biometricTemp
    if request.method == "POST":
        sessionKey = session.get('session_key')
        if sessionKey == None:
            return jsonify({'status': 'fail'}) # Return fail if session out
        else:
            sessionUser = session.get('profile')['userId'] # Select user id from session
            data= request.get_json()
            data['user'] = session.get('profile')['userId'] # Select user id from session
            structure = json.loads(str(json.dumps(data))) # Create json stucture with user id
            # Check if current behaviour goes more than 18 or not
            if behaviour >= 18:
                print(f'In Behaviour End State {len(biometricTemp)}')
                # Check if suspicious behaviour goes more than 18 or not
                if len(biometricTemp) >= 18:
                    modelVal = str(Validation(sessionUser,biometricTemp)) # Check into model that is imposter or not
                    print('Final',type(modelVal))
                    #If imposter then it will retunr imposter status and logout from the system othe wise continue 
                    if modelVal == 'imposter':
                        print('In Imposter')
                        return jsonify({'status': 'imposter'})
                    else:
                        print('In User')
                        keyCollection.insert_many(biometricTemp)
                        print('Prediction:',modelVal)
                        biometricTemp = []
                        return jsonify({'status': str(modelVal)})
                else:
                    biometricTemp.append(structure) # Add single data to queue to check
                    return jsonify({'status': 'continue'})
            else:
                print(f'In Behaviour State {behaviour}')
                behaviour += 1
                keyCollection.insert_one(structure) # Add single data for current behaviour
                return jsonify({'status': 'continue'})

@app.route('/logout')
def logout():
    # Logout system witn massage and session logout system
    session.clear()
    custMessage = 'All Done! Good Bye';
    return render_template('logout.html', message=custMessage)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

# Custome Validation function
class Validate:
    def valText(text):
        rtext = re.match(r'^([a-zA-Z])\D+', text)
        print(rtext)
        if bool(rtext) == True:
            return text
        else:
            return ' '
    def valEmail(email):
        remail= re.match(r'^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$', email)
        if bool(remail) == True:
            return email
        else:
            return ' '

# Name Combining Function
def combine(first,middle,last):
    name = ' '
    if first != ' ':
        name += str(first)
    if middle != ' ':
        name += ' ' + str(middle)
    if last != ' ':
        name += ' ' + str(last)
    name = name.lstrip()
    return name

    

