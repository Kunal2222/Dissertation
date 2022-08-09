import config
import re
import pymongo
import json
from flask import Flask, redirect, url_for, render_template, request, flash
from pymongo import MongoClient
from flask_bcrypt import Bcrypt

app = Flask(__name__)

'''Production Configuration'''
#app.config.from_object('config.ProdConfig')

'''Development Configuration'''
app.config.from_object('config.DevConfig')

bcrypt = Bcrypt(app)

uri = 'mongodb+srv://continuesauth.gqcdh.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&ssl=true'

client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='static/certificate/X509-cert-666372965419332429.pem')

db = client['dissertation']
userCollection = db['users']
keyCollection = db['keystrock_dynamics']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registration')
def registration():
    return render_template('registration_form.html')


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
            hasedUserPassword = bcrypt.generate_password_hash(userPassword)
            #if Bcrypt.check_password_hash(userPassword, dbPassword):
            checkPassword = bcrypt.check_password_hash(dbPassword, userPassword)
            if checkPassword == True:
                print('Successfully Loggedin')
        else:
            alert = [{"type":"danger","name":"Error","description":"User Doesn't Exist."}]
            return render_template('index.html', alert=alert)
        return redirect(url_for('dashboard'))

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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/auth', methods=['GET','POST'])
def auth():
     data=None
     if request.method == "POST":
          data= request.get_json()
          structure = json.loads(str(json.dumps(data)))
          print(structure)
          keyCollection.insert_one(structure)
     return 'Sucess'

@app.route('/logout')
def logout():
    return render_template('logout.html')

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

    

