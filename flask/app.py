import time
import os
from urllib import request
import pandas as pd
from autoARIMA import AutoArima
from linearRegression import linearRegressionClass
from randomForest import randomForestClass
from xgb import XGBClass 
from multinomialNaiveBayes import MultinomialNaiveBayesClass
# from ProphetAPI import ProphetClass
from dateGen import DateGen
# from rnn import Rnn
# from ML import MLModelsClass
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS

UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

STORAGES_LIST = ['Storage 1', 'Storage 2', 'Storage 3', 'Storage 4']

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
        'message': 'Flask Running'
    }

@app.route('/autoarima/train',methods=['POST'])
def autoarima_train():
    file = request.files['file'] 
    df = pd.read_csv(file)
    df = AutoArima.preprocess(df,1)
    AutoArima.train(df)
    return "Model Trained Successfully"
    # preds = AutoArima.predict(test)
    # print(preds)
    # response=preds
    # return response.to_csv()


@app.route('/autoarima/update',methods=['POST'])
def autoarima_update():
    file = request.files['file'] 
    df = pd.read_csv(file)
    df = AutoArima.preprocess(df,1)
    AutoArima.update(df)
    return "Updated Model Successfully"

@app.route('/autoarima/predict',methods=['POST'])
def autoarima_predict():
    file = request.files['file'] 
    df = pd.read_csv(file)
    df = AutoArima.preprocess(df,1)
    preds = AutoArima.predict(df[:50])
    # print(preds)
    response=preds
    return response.to_csv()

@app.route('/prophet',methods=['POST'])
def prophet():
    # file = request.files['file'] 
    # df = pd.read_csv(file)
    # df = ProphetClass.preprocess(df)
    # test = ProphetClass.train(df)
    # preds = ProphetClass.predict(test)
    # print(preds)
    # response = preds
    # return response.to_csv()
    return 'prophet'

@app.route('/rnn',methods=['POST'])
def rnn():
    file = request.files['file'] 
    df = pd.read_csv(file)
    preds = Rnn.model(df)
    print(preds)
    response = preds
    return response.to_csv()
    # return "rnn"

@app.route('/mlmodels',methods=['POST'])
def MLModels():
    file = request.files['file'] 
    df = pd.read_csv(file)
    preds = MLModelsClass.model(df)
    print(preds)
    response = preds
    return response.to_csv()  

@app.route('/linearRegression',methods=['POST'])
def linearRegression():
    file = request.files['file'] 
    df = pd.read_csv(file)
    preds = linearRegressionClass.model(df)
    print(preds)
    response = preds
    return response.to_csv()     

@app.route('/randomForest',methods=['POST'])
def randomForest():
    file = request.files['file'] 
    df = pd.read_csv(file)
    preds = randomForestClass.model(df)
    print(preds)
    response = preds
    return response.to_csv()       

@app.route('/XGB',methods=['POST'])
def XGB():
    file = request.files['file'] 
    df = pd.read_csv(file)
    preds = XGBClass.model(df)
    print(preds)
    response = preds

@app.route('/MultinomialNaiveBayes',methods=['POST'])
def MultinomialNaiveBayes():
    file = request.files['file'] 
    df = pd.read_csv(file)
    preds = MultinomialNaiveBayesClass.model(df)
    print(preds)
    response = preds    

@app.route('/dateGen',methods=['GET'])
def dategenerator():
    df = DateGen.date_df(5,1)
    response = df
    return response.to_csv()


@app.route('/liststorages')
def list_storages():
    return{
        'resultStatus': 'SUCCESS',
        'message': ','.join(STORAGES_LIST)
    }

