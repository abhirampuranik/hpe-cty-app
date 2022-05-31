import time
import os
from urllib import request
import pandas as pd
from autoARIMA import AutoArima
from ProphetAPI import ProphetClass
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
def autoarima():
    file = request.files['file'] 
    df = pd.read_csv(file)
    df = AutoArima.preprocess(df)
    test = AutoArima.train(df)
    preds = AutoArima.predict(test)
    print(preds)
    response=preds
    return "preds"

@app.route('/prophet',methods=['POST'])
def prophet():
    file = request.files['file'] 
    df = pd.read_csv(file)
    df = ProphetClass.preprocess(df)
    test = ProphetClass.train(df)
    preds = ProphetClass.predict(test)
    print(preds)
    response = preds
    return "preds"

@app.route('/rnn',methods=['POST'])
def prophet():
    file = request.files['file'] 
    df = pd.read_csv(file)
    df = ProphetClass.preprocess(df)
    test = ProphetClass.train(df)
    preds = ProphetClass.predict(test)
    print(preds)
    response = preds
    return "preds"

