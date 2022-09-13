'''
Programe Name: Machine Learning model to generate the prediction
Supervisor: Andrew Stratton
Purpose: Dissertation Thesis
Organisation: University of Sheffield
Developer: Kunal Das
'''
'''Add Liabries'''
import re
import pandas as pd
import numpy as np
from scipy.stats import zscore
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_curve, accuracy_score, classification_report, confusion_matrix

import pymongo
from pymongo import MongoClient

# MongoDB url
uri = 'mongodb+srv://continuesauth.gqcdh.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&ssl=true'

# Mongodd connection with token
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='static/certificate/X509-cert-666372965419332429.pem')

db = client['dissertation'] # Database Selection
keyCollection = db['keystrock_dynamics'] # Collection

class Validation:
  def __init__(self, userId, data):
    self.userId= userId # Getting User Id
    self.data = data # Getting User Data
    self.dataCollect() # Run the first step for data preprocession
    self.normalize() # Data Normalization
    self.trainig() # Train the model
    self.predictionVal = self.prediction() # Generate the prediction
  def __str__(self):
    print(self.predictionVal.strip())
    return self.predictionVal.strip() # Return the prediction
    
  # Custome label replace for user labels to imposter label
  def labelReplace(self,data,label):
    testSeries = []
    for val in data['user']: # Select each user data
      changeVal = re.sub(r'.*[a-zA-Z0-9]', label, val) # replace labels using regular expression
      testSeries.append(changeVal) # Added that to the series
    testSeries = pd.DataFrame(testSeries) # Create the dataset into data frame
    testSeries.columns = ['user'] # Add cloumn name
    return testSeries # return the updated dataset

  def dataCollect(self):
    biometrics = keyCollection.find({'user':self.userId}) # Collect actual user data from database
    impBiometrics = keyCollection.find({'user':{ '$nin': [self.userId] }}) # Collect rest of the users details 
    

    self.dataFrame = pd.DataFrame.from_dict(biometrics, orient='columns') # Covent into pandas Dataframe
    self.dataFrame = self.dataFrame.mask(self.dataFrame==0).fillna(self.dataFrame.mean()) # Replace 0 with Mean

    self.impDataFrame = pd.DataFrame.from_dict(impBiometrics, orient='columns') # Covent into pandas Dataframe
    self.impDataFrame = self.impDataFrame.mask(self.impDataFrame==0).fillna(self.impDataFrame.mean()) # Replace 0 with Mean

    self.suspiciousData = pd.DataFrame.from_dict(self.data, orient='columns') # Covent into pandas Dataframe
    self.suspiciousData = self.suspiciousData.mask(self.suspiciousData==0).fillna(self.suspiciousData.mean()) # Replace 0 with Mean

  def normalize(self):
    dfFeatures = self.dataFrame.iloc[:,1:-1] # Select only the rows with data
    impdfFeatures = self.impDataFrame.iloc[:,1:-1] # Select only the rows with data
    suspiciousFeatures = self.suspiciousData.iloc[:, :-1] # Select only the rows with data


    self.dfNormalize = zscore(dfFeatures) # normalize the data with zscore normalization
    self.impDfNormalize = zscore(impdfFeatures) # normalize the data with zscore normalization
    self.suspiciousDataNormalize = zscore(suspiciousFeatures) # normalize the data with zscore normalization

    self.dfLabels = self.dataFrame.iloc[:,-1:] # select the lables of that data
    self.impDfLabels = self.impDataFrame.iloc[:,-1:] # select the lables of that data
    self.suspiciousLaels = self.suspiciousData.iloc[:,-1:] # select the lables of that data

  def trainig(self):
    
    scaler = StandardScaler() # Select Standard Scaler

    limit = 50 # Set a limit for the dataset to balance between two datasets

    print(f'Dataframe Count: {len(self.dfNormalize)}')
    print(f'Dataframe Label Count: {len(self.dfLabels)}')

    print(f'Imposter Count: {len(self.impDfNormalize)}')
    print(f'Imposter Label Count: {(self.impDfLabels)}')
    
    # Select a limited amount of dataset if it's less than that then it will select the length of the actual data set
    if len(self.dfNormalize) >= 50:
      self.dfNormalize = self.dfNormalize.sample(n = 50)
      self.dfLabels = self.dfLabels.sample(n = 50)

      self.impDfNormalize = self.impDfNormalize.sample(n = 50)
      self.impDfLabels = self.impDfLabels.sample(n = 50)
    else:
      self.impDfNormalize = self.impDfNormalize.sample(n = len(self.dfNormalize))
      self.impDfLabels = self.impDfLabels.sample(n = len(self.dfNormalize))
    
    print(f'Dataframe Count: {len(self.dfNormalize)}')
    print(f'Dataframe Label Count: {len(self.dfLabels)}')

    print(f'Imposter Count: {len(self.impDfNormalize)}')
    print(f'Imposter Label Count: {(self.impDfLabels)}')

    xTrain, xTest, yTrain, yTest = train_test_split(self.dfNormalize, self.dfLabels, test_size=0.2, random_state = 4) # Split actual dataset
    impXTrain, impXTest, impYTrain, impYTest = train_test_split(self.impDfNormalize, self.impDfLabels, test_size=0.6, random_state = 4) # Split imposter dataset

    tempData = self.labelReplace(impYTrain,'imposter') # Replace imposter labels

    xTrain = xTrain.append(impXTrain, ignore_index=True) # Append imposter data into actual dataset
    yTrain = yTrain.append(tempData, ignore_index=True)# Append imposter labels into actual label

    # Set a random state
    xTrain = xTrain.sample(frac=1, random_state=1).reset_index(drop=True)
    yTrain = yTrain.sample(frac=1, random_state=1).reset_index(drop=True)


    scaler.fit(xTrain)
    xTrain = scaler.transform(xTrain) #real user train data
    
    self.knn = KNeighborsClassifier(n_neighbors=5) # Set Cluster Size
    self.knn.fit(xTrain, yTrain) # Fit model for training
    self.suspiciousDataNormalize = scaler.transform(self.suspiciousDataNormalize) # Scale suspicious data

  def prediction(self):
    
    testLength = len(self.suspiciousDataNormalize) # Get the length of suspicious data

    self.yPred = self.knn.predict(self.suspiciousDataNormalize) # Predict with the suspicious dat


    confusionMatrix = confusion_matrix(self.suspiciousLaels, self.yPred) # Generate confusion matrix
    score = accuracy_score(self.suspiciousLaels, self.yPred) # Get the score of the prediction
    report = classification_report(self.suspiciousLaels, self.yPred , output_dict=True) # Generate Classification report
    
    reportDf = df = pd.DataFrame(report) # Convert that report into data frame

    falsePositive = confusionMatrix.sum(axis=0) - np.diag(confusionMatrix) # Calculate false postive
    support = int(100 * falsePositive[1]/ testLength) # Calculate support based on fasle positie
    score = int(score * 100) 
    print(f'Support:{support},Score:{score}')
    # if support of imposter getter than 40 or score < 60 predict as an imposter
    if support > 40 or score < 60:
      print('imposter')
      return 'imposter'
    else:
      print('user')
      return 'user'