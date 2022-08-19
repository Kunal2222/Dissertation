import pickle
import pandas as pd
import numpy as np
from scipy.stats import zscore
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve
from sklearn.metrics import accuracy_score

import pymongo
from pymongo import MongoClient

uri = 'mongodb+srv://continuesauth.gqcdh.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&ssl=true'

client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='static/certificate/X509-cert-666372965419332429.pem')

db = client['dissertation']
keyCollection = db['keystrock_dynamics']

class Validation:
  def __init__(self, userId, data):
    self.userId= userId
    self.data = data
    print(userId, data)
