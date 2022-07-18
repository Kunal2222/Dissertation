import os
from flask import Flask, redirect, url_for, render_template ,request,flash
app=Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY')
@app.route("/")
def index():
    return render_template('index.html')