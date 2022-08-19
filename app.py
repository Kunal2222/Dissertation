from copyreg import pickle
from datetime import timedelta
from email import message
import calendar
import time
from datetime import datetime
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


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(MyEncoder, self).default(obj)

uri = 'mongodb+srv://continuesauth.gqcdh.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&ssl=true'


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

bcrypt = Bcrypt(app)

client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='static/certificate/X509-cert-666372965419332429.pem')

db = client['dissertation']
userCollection = db['users']
keyCollection = db['keystrock_dynamics']
mouseCollection = db['mouse_dynamics']
sessionCollection = db['session']

#model = pickle.load(open('model.pkl', 'rb'))

 
behaviour = 0
validator = 0
biometricTemp = []

mouseBehaviour = 0
mouseValidator = 0
mouseBiometricTemp = []

@app.before_request
def sessionHandle():
    if session.get('session_key') != None:
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=5)
        g.profile = session.get('profile')
        

@app.route('/')
def index():
    sessionKey = session.get('session_key')
    print(f'Session Index Key:{sessionKey}')
    if sessionKey == None:
        return render_template('index.html')
    else:
        print('Session',session.get('session_key'))
        return redirect(url_for('dashboard'))
        


@app.route('/registration')
def registration():
    sessionKey = session.get('session_key')
    print(f'Session Registration Key:{sessionKey}')
    if sessionKey == None:
        return render_template('registration_form.html')
    else:
        return redirect(url_for('dashboard'))


@app.route('/security', methods=['POST', 'GET'])
def authentication():
    if request.method == 'POST':
        userEmail = request.form['user_email']
        userPassword = request.form['user_pwd']

        inputEmail = re.match(r'^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$', userEmail)
        if bool(inputEmail) == True:
            userEmail = userEmail.lower()

        myquery = {'email': userEmail}
        checkUser = userCollection.count_documents(myquery);
        if checkUser > 0:
            userData = userCollection.find(myquery)
            dbPassword = userData[0]['password']
            dbUserId = userData[0]['_id']
            dbUserName = userData[0]['fullName']
            dbUserId = json.loads(json_util.dumps(dbUserId))['$oid']
            print(dbUserName)
            hasedUserPassword = bcrypt.generate_password_hash(userPassword)
            checkPassword = bcrypt.check_password_hash(dbPassword, userPassword)
            if checkPassword == True:
                print(dbUserId)
                session['session_key'] = uuid.uuid4().hex[:20]
                session['profile'] = {"userId": dbUserId, "userName": dbUserName}
                gmt = time.gmtime()
                timeStamp = calendar.timegm(gmt)
                dataTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                sessionEntry = sessionCollection.insert_one({'sessionKey':session.get('session_key'), 'name': session.get('profile')['userName'], 'userId': session.get('profile')['userId'], 'datetime':dataTime, 'timestamp': timeStamp})
                return redirect(url_for('dashboard'))
            else:
                session.clear()
                alert = [{"type":"warning","name":"Invalid","description":"Username or Password!"}]
                return render_template('index.html', alert=alert)
        else:
            session.clear()
            alert = [{"type":"danger","name":"Error","description":"User Doesn't Exist."}]
            return render_template('index.html', alert=alert)

@app.route('/submit-details', methods=['POST', 'GET'])
def user_registration():
    if request.method == 'POST':
        firstName = Validate.valText(request.form['first_name'])
        middleName = Validate.valText(request.form['middle_name'])
        lastName = Validate.valText(request.form['last_name'])
        fullName = combine(firstName,middleName,lastName)
        email = Validate.valEmail(request.form['email'])
        email = email.lower()
        checkEmail = {'email': email}
        checkUser = userCollection.count_documents(checkEmail);
        if checkUser > 0:
            alert = [{"type":"warning","name":"Warning","description":"User Already Exist."}]
            return render_template('registration_form.html', alert=alert)
        password = bcrypt.generate_password_hash(request.form['pwd'])
        entry = userCollection.insert_one(
            {'fullName':fullName, 'firstName': firstName, 'middleName': middleName, 'lastName': lastName, 'email': email, 'password': password})
        return redirect(url_for('index'))

@app.route('/read')
def read():
    sessionKey = session.get('session_key')
    print(f'Session Read Key:{sessionKey}')
    if sessionKey == None:
        session.clear()
        custMessage = 'Sorry! Session Out';
        return render_template('logout.html', message=custMessage)
    else:
        return render_template('read.html')

@app.route('/dashboard')
def dashboard():
    sessionKey = session.get('session_key')
    print(f'Session Dashboard Key:{sessionKey}')
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
        if session.get('session_key') != None:
            #modelVal = Validation('1','Started')
            sessionUser = session.get('profile')['userId']
            data= request.get_json()
            data['user'] = session.get('profile')['userId']
            structure = json.loads(str(json.dumps(data)))
            if mouseBehaviour >= 100:
                if len(mouseBiometricTemp) >= 18:
                    return 'Success'
                else:
                    mouseBiometricTemp.append(structure)
                    print(mouseBiometricTemp)
                    return 'Continue'
            else:
                mouseBehaviour += 1
                mouseCollection.insert_one(structure)
                return 'Continue'

@app.route('/auth', methods=['GET','POST'])
def auth():
    global behaviour
    global validator
    global biometricTemp
    if request.method == "POST":
        if session.get('session_key') != None:
            modelVal = Validation('1','Started')
            sessionUser = session.get('profile')['userId']
            data= request.get_json()
            data['user'] = session.get('profile')['userId']
            structure = json.loads(str(json.dumps(data)))
            if behaviour >= 100:
                if len(biometricTemp) >= 18:
                    return 'Success'
                else:
                    biometricTemp.append(structure)
                    print(biometricTemp)
                    return 'Continue'
            else:
                behaviour += 1
                keyCollection.insert_one(structure)
                return 'Continue'

@app.route('/logout')
def logout():
    session.clear()
    custMessage = 'All Done! Good Bye';
    return render_template('logout.html', message=custMessage)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

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

    

