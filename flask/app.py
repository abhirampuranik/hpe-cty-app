import time
import os
from urllib import request
import pandas as pd
from autoarima import AutoArima
# from flask import Flask
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS

UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

app = Flask(__name__)
CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/time')
def get_current_time():
    return {
      'resultStatus': 'SUCCESS',
      'message': time.time()
      }

@app.route('/hello')
def hello_get():
    return{
        'resultStatus': 'SUCCESS',
        'message': 'Hello boi'
    }

@app.route('/autoarima',methods=['POST'])
def fileUpload():
    file = request.files['file'] 
    df = pd.read_csv(file)
    df = AutoArima.preprocess(df)
    test = AutoArima.train(df)
    preds = AutoArima.predict(test)
    print(preds)
    # session['uploadFilePath']=destination
    print( "coming here",file)
    response="Whatever you wish too return"
    return response








# def auto_arima_post():
#     # if request.method == 'POST':
#     # print(request.FileHandler)
#     # print(dir(request.http))
#     # print(request)
#     # file = request.FileHandler['file']
#     file = request.files['file']
#     print(file)
#     return "done"
        

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import pickle

# class AutoArima:
#     def __init__(csv):
#         pass
    
#     def preprocess(df):
#         dataset = df
#         df_User1 = dataset[dataset['UserID']==1]
#         df_User1.index = df_User1['Time']
#         df = df_User1.drop(['Time','UserID'],axis=1)
#         print(df)
#         return df

#     def train(df):
#         test_size = 50
#         test_ind = len(df) - test_size
#         train = df.iloc[:test_ind]
#         test = df.iloc[test_ind:]

#         from pmdarima.arima import auto_arima
#         arima_model = auto_arima(train, start_p=0, d=1, start_q=0,
#         max_p=5, max_d=5, max_q=5, start_P=0,
#         D=1, start_Q=0, max_P=5, max_D=5,
#         max_Q=5, m=12, seasonal=True,
#         error_action='warn',trace = True,
#         supress_warnings=True, stepwise = True,
#         random_state=20,n_fits = 50)
#         arima_model.summary()
#         with open('arima.pkl', 'wb') as pkl:
#             pickle.dump(arima_model, pkl)
#         return test
    
#     def predict(test):
#         with open('arima.pkl', 'rb') as pkl:
#             prediction = pd.DataFrame(pickle.load(pkl).predict(n_periods=test_size),index=test.index)
#             prediction.columns = ['forecast']
#             print(prediction)
#             return prediction
#     def update(df):
#         with open('arima.pkl', 'rb') as pkl:
#             pickle.load(pkl).update(df)