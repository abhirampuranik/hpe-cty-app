import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import random
import re
import time
from datetime import datetime, timedelta
from pandas import to_datetime
import matplotlib.pyplot as plt
from matplotlib.style import use
import numpy as np
from fbprophet import Prophet
import pickle

class ProphetClass:
    def __init__():
        pass
    
    def preprocess(df, userID):
        dataset = df
        if(userID in set(dataset['UserID'])):
          df_User1 = dataset[dataset['UserID']==userID]
          df1 = df_User1
          df1 = df1.rename(columns={'Usage': 'y', 'Time': 'ds'})
          df1.drop('UserID', inplace=True, axis=1)
          #print("UserID exists!\n",df1)
        else:
          df2 = dataset 
          df2 = df2.rename(columns={'Usage': 'y', 'Time': 'ds'})
          df2.drop('UserID', inplace=True, axis=1)
          df1 = df2
          #print("UserID does not exist!\n",df1)
        df1['ds']= to_datetime(df1['ds'])
        return df1

    def train(df):
        #test_size = int(len(df)*0.2)
        test_size = 0
        test_ind = len(df) - test_size
        train = df.iloc[:test_ind]
        #test = df.iloc[test_ind:]

        prophet_model = Prophet()
        prophet_model.fit(train)
        with open('prophet.pkl', 'wb') as pkl:
            pickle.dump(prophet_model, pkl)
        #return test
    
    def predict(test):
        test_size = len(test)
        with open('prophet.pkl', 'rb') as pkl:
            prophet_model = pickle.load(pkl)
            future = test['ds']
            future = pd.DataFrame(future)
            future.columns = ['ds']
            future['ds']= to_datetime(future['ds'])
            prediction = prophet_model.predict(future)
            prediction = prediction[['ds','yhat']]
            prediction.rename(columns = {'ds':'Time', 'yhat':'Usage'}, inplace = True)
            #prediction.set_index('Time', inplace=True)
            return prediction


'''class ProphetClass:
    def __init__():
        pass
    
    def preprocess(df, userID):
        #dataset = df
        #df_User1 = dataset[dataset['UserID']==userID]
        #df = df_User1
        #df = df.rename(columns={'Usage': 'y', 'Time': 'ds'})
        #df.drop('UserID', inplace=True, axis=1)
        #df['ds']= to_datetime(df['ds'])
        #return df
        dataset = df
        if(userID in set(dataset['UserID'])):
          df_User1 = dataset[dataset['UserID']==userID]
          df1 = df_User1
          df1 = df1.rename(columns={'Usage': 'y', 'Time': 'ds'})
          df1.drop('UserID', inplace=True, axis=1)
          #print("UserID exists!\n",df1)
        else:
          df2 = dataset 
          df2 = df2.rename(columns={'Usage': 'y', 'Time': 'ds'})
          df2.drop('UserID', inplace=True, axis=1)
          df1 = df2
          #print("UserID does not exist!\n",df1)
        df1['ds']= to_datetime(df1['ds'])
        return df1

    def train(df):
        test_size = int(len(df)*0.2)
        test_ind = len(df) - test_size
        train = df.iloc[:test_ind]
        test = df.iloc[test_ind:]

        prophet_model = Prophet()
        prophet_model.fit(train)
        with open('prophet.pkl', 'wb') as pkl:
            pickle.dump(prophet_model, pkl)
        return test
    
    def predict(test):
        test_size = len(test)
        with open('prophet.pkl', 'rb') as pkl:
            prophet_model = pickle.load(pkl)
            future = test['ds']
            future = pd.DataFrame(future)
            future.columns = ['ds']
            future['ds']= to_datetime(future['ds'])
            prediction = prophet_model.predict(future)
            prediction = prediction[['yhat','ds']]
            prediction.rename(columns = {'ds':'Time', 'yhat':'forecast'}, inplace = True)
            prediction.set_index('Time', inplace=True)
            return prediction
'''



  
