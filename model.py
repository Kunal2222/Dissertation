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
    self.dataCollect()
    self.normalize()
    self.trainig()
    self.predictionVal = self.prediction()
  def __str__(self):
    print(self.predictionVal.strip())
    return self.predictionVal.strip()
    

  def labelReplace(self,data,label):
    testSeries = []
    for val in data['user']:
      changeVal = re.sub(r'.*[a-zA-Z0-9]', label, val)
      testSeries.append(changeVal)
    testSeries = pd.DataFrame(testSeries)
    testSeries.columns = ['user']
    return testSeries

  def dataCollect(self):
    biometrics = keyCollection.find({'user':self.userId})
    impBiometrics = keyCollection.find({'user':{ '$nin': [self.userId] }})
    

    self.dataFrame = pd.DataFrame.from_dict(biometrics, orient='columns')
    self.dataFrame = self.dataFrame.mask(self.dataFrame==0).fillna(self.dataFrame.mean())

    self.impDataFrame = pd.DataFrame.from_dict(impBiometrics, orient='columns')
    self.impDataFrame = self.impDataFrame.mask(self.impDataFrame==0).fillna(self.impDataFrame.mean())

    self.suspiciousData = pd.DataFrame.from_dict(self.data, orient='columns')
    self.suspiciousData = self.suspiciousData.mask(self.suspiciousData==0).fillna(self.suspiciousData.mean())

  def normalize(self):
    dfFeatures = self.dataFrame.iloc[:,1:-1]
    impdfFeatures = self.impDataFrame.iloc[:,1:-1]
    suspiciousFeatures = self.suspiciousData.iloc[:, :-1]


    self.dfNormalize = zscore(dfFeatures)
    self.impDfNormalize = zscore(impdfFeatures)
    self.suspiciousDataNormalize = zscore(suspiciousFeatures)

    self.dfLabels = self.dataFrame.iloc[:,-1:]
    self.impDfLabels = self.impDataFrame.iloc[:,-1:]
    self.suspiciousLaels = self.suspiciousData.iloc[:,-1:]

  def trainig(self):
    
    scaler = StandardScaler()

    limit = 50

    print(f'Dataframe Count: {len(self.dfNormalize)}')
    print(f'Dataframe Label Count: {len(self.dfLabels)}')

    print(f'Imposter Count: {len(self.impDfNormalize)}')
    print(f'Imposter Label Count: {(self.impDfLabels)}')
    
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

    xTrain, xTest, yTrain, yTest = train_test_split(self.dfNormalize, self.dfLabels, test_size=0.2, random_state = 4)
    impXTrain, impXTest, impYTrain, impYTest = train_test_split(self.impDfNormalize, self.impDfLabels, test_size=0.6, random_state = 4)

    tempData = self.labelReplace(impYTrain,'imposter')

    xTrain = xTrain.append(impXTrain, ignore_index=True) 
    yTrain = yTrain.append(tempData, ignore_index=True)

    xTrain = xTrain.sample(frac=1, random_state=1).reset_index(drop=True)
    yTrain = yTrain.sample(frac=1, random_state=1).reset_index(drop=True)

    scaler.fit(xTrain)
    xTrain = scaler.transform(xTrain) #real user train data
    
    self.knn = KNeighborsClassifier(n_neighbors=5)
    self.knn.fit(xTrain, yTrain)
    self.suspiciousDataNormalize = scaler.transform(self.suspiciousDataNormalize)

  def prediction(self):
    
    testLength = len(self.suspiciousDataNormalize)

    self.yPred = self.knn.predict(self.suspiciousDataNormalize)


    confusionMatrix = confusion_matrix(self.suspiciousLaels, self.yPred)
    score = accuracy_score(self.suspiciousLaels, self.yPred)
    report = classification_report(self.suspiciousLaels, self.yPred , output_dict=True)
    
    reportDf = df = pd.DataFrame(report)

    falsePositive = confusionMatrix.sum(axis=0) - np.diag(confusionMatrix)
    support = int(100 * falsePositive[1]/ testLength)
    score = int(score * 100)
    print(f'Support:{support},Score:{score}')
    if support > 40 or score < 60:
      print('imposter')
      return 'imposter'
    else:
      print('user')
      return 'user'