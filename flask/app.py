from operator import index
import time
import os
from urllib import request
import pandas as pd
from sqlalchemy import false
from autoARIMA import AutoArima
from linearRegression import linearRegressionClass
from randomForest import randomForestClass
from xgb import XGBClass 
from multinomialNaiveBayes import MultinomialNaiveBayesClass
# from ProphetAPI import ProphetClass
from dateGen import DateGen
from dateGenML import DateGenML
from DateGenP import DateGenP
from rnn import Rnn
# from ML import MLModelsClass
from flask import Flask, flash, request, redirect, url_for, session, Response
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

@app.route('/data',methods=['POST'])
def data():
    file = request.files['file'] 
    userID = int(request.form['userID'])
    df = pd.read_csv(file)
    df = df[df['UserID'] == userID]
    return df.to_csv(index=False)

@app.route('/datalinearreg',methods=['POST'])
def dataLinearReg():
    file = request.files['file'] 
    userID = int(request.form['userID'])
    df = pd.read_csv(file)
    df = df[df['UserID'] == userID]
    df = df[:-769]
    return df.to_csv(index=False)


@app.route('/stream',methods=['GET'])
def stream():
    df = pd.read_csv("storage_train.csv")
    df_prep = AutoArima.preprocess(df,1)
    dg = DateGen()
    AutoArima.train(df_prep[:50])
    def getdata():
        # file = request.files['file'] 
        
        for i in range(50,len(df_prep)):
            AutoArima.update(df_prep[i:i+1])
            df = dg.date_df(5,1,df_prep.index[i])
            preds = AutoArima.predict(df)
            final_df = df_prep[49:i].append(preds)
            s = final_df.to_csv().replace('\r\n', '$')
            #gotcha
            yield f'data: {s} \n\n' 
            time.sleep(1)
            
    response = Response(getdata(), mimetype='text/event-stream')

    response.headers['Content-Disposition'] = 'inline'
    # response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    return response

# @app.route('/stream',methods=['GET'])
# def stream():
#     dg = DateGen()
#     # file = request.files['file'] 
#     df = pd.read_csv("storage_train.csv")
#     df_prep = linearRegressionClass.preprocess(df,1)
#     linearRegressionClass.train(df_prep[:50])
#     for i in range(50,len(df_prep)):
#         linearRegressionClass.update(df_prep[i:i+1])
#         df = dg.date_df(10,1)
#         preds = linearRegressionClass.predict(df)
#         print(preds)
#         print(df_prep[i-5:i])
        
#         final_df = df_prep[i-5:i].append(preds)
#         print(final_df)
#         time.sleep(10)
#     return "Model Streaming"


# AutoArima

@app.route('/autoarima/train',methods=['POST'])
def autoarima_train():
    file = request.files['file']
    userID = int(request.form['userID'])
    df = pd.read_csv(file)
    df = AutoArima.preprocess(df,userID)
    AutoArima.train(df)
    return "Model Trained Successfully"

@app.route('/autoarima/update',methods=['POST'])
def autoarima_update():
    file = request.files['file'] 
    userID = int(request.form['userID'])
    df = pd.read_csv(file)
    df = AutoArima.preprocess(df,userID)
    AutoArima.update(df)
    return "Updated Model Successfully"

@app.route('/autoarima/predict',methods=['POST'])
def autoarima_predict():
    days = request.json['body']['days']
    hours = request.json['body']['hours']
    userID = request.json['body']['userID']
    dg = DateGen()
    fil = open('arima.txt','r')
    df = dg.date_df(int(days)*24 + int(hours), int(userID),fil.readline().strip())
    fil.close()
    preds = AutoArima.predict(df)
    response=preds
    return response.to_csv()


# Linear Regression

@app.route('/linearRegression/train',methods=['POST'])
def linearRegression_train():
    file = request.files['file']
    userID = int(request.form['userID'])
    df = pd.read_csv(file)    
    df = linearRegressionClass.preprocess(df,userID,"train")
    linearRegressionClass.train(df)
    return "Model Trained Successfully"   

@app.route('/linearRegression/predict',methods=['POST'])
def linearRegression_predict():
    days = request.json['body']['days']
    hours = request.json['body']['hours']
    userID = request.json['body']['userID']
    #file = request.files['file']
    df = pd.read_csv('LR_Predict.csv')
    hrs=int(days)*24 + int(hours)
    df = linearRegressionClass.preprocess(df,int(userID),"predict")
    preds = linearRegressionClass.predict(df,hrs)    
    response=preds       
    return response.to_csv(index=False)    

# Random Forest

@app.route('/randomForest/train',methods=['POST'])
def randomForest_train():
    file = request.files['file'] 
    df = pd.read_csv(file)
    df = randomForestClass.preprocess(df)
    test = randomForestClass.train(df)
    preds = randomForestClass.predict(test)
    print(preds)
    response=preds
    return response.to_csv() 

@app.route('/randomForest/update',methods=['POST'])
def randomForest():
    file = request.files['file'] 
    df = pd.read_csv(file)
    df = randomForestClass.preprocess(df)
    randomForestClass.update(df)
    return "Updated Model Successfully" 

@app.route('/randomForest/predict',methods=['POST'])
def randomForest_predict():
    file = request.files['file'] 
    df = pd.read_csv(file)
    df = randomForestClass.preprocess(df)
    preds = randomForestClass.predict(df[:50])
    # print(preds)
    response=preds
    return response.to_csv()


#MNB

@app.route('/multinomialNaiveBayes/train',methods=['POST'])
def multinomialNaiveBayes_train():
    file = request.files['file'] 
    df = pd.read_csv(file)
    df = MultinomialNaiveBayesClass.preprocess(df)
    test = MultinomialNaiveBayesClass.train(df)
    preds = MultinomialNaiveBayesClass.predict(test)
    print(preds)
    response=preds
    return response.to_csv() 

@app.route('/multinomialNaiveBayes/update',methods=['POST'])
def multinomialNaiveBayes_update():
    file = request.files['file'] 
    df = pd.read_csv(file)
    df = MultinomialNaiveBayesClass.preprocess(df)
    MultinomialNaiveBayesClass.update(df)
    return "Updated Model Successfully" 


@app.route('/multinomialNaiveBayes/predict',methods=['POST'])
def multinomialNaiveBayes_predict():
    file = request.files['file'] 
    df = pd.read_csv(file)
    df = MultinomialNaiveBayesClass.preprocess(df)
    preds = MultinomialNaiveBayesClass.predict(df[:50])
    # print(preds)
    response=preds
    return response.to_csv()



# XGB

@app.route('/xgb/train',methods=['POST'])
def xgb_train():
    file = request.files['file'] 
    df = pd.read_csv(file)
    df = XGBClass.preprocess(df)
    test = XGBClass.train(df)
    preds = XGBClass.predict(test)
    print(preds)
    response=preds
    return response.to_csv()               


@app.route('/xgb/update',methods=['POST'])
def xgb_update():
    file = request.files['file'] 
    df = pd.read_csv(file)
    df = XGBClass.preprocess(df)
    XGBClass.update(df)
    return "Updated Model Successfully"              

@app.route('/xgb/predict',methods=['POST'])
def xgb_predict():
    file = request.files['file'] 
    df = pd.read_csv(file)
    df = XGBClass.preprocess(df)
    preds = XGBClass.predict(df[:50])
    # print(preds)
    response=preds
    return response.to_csv()

# Prophet

@app.route('/prophet/train',methods=['POST'])
def prophet_train():
      file = request.files['file'] 
      userID = int(request.form['userID'])
      df = pd.read_csv(file)
      df = ProphetClass.preprocess(df, userID)
      ProphetClass.train(df)
      return 'Prophet trained Successfully'

@app.route('/prophet/predict',methods=['POST'])
def prophet_predict():
        # print("test"+request.body)
        try:
            days = request.json['body']['days']
            hours = request.json['body']['hours']
            userID = request.json['body']['userID']
        #df = ProphetClass.preprocess(df, userID)
        #test = ProphetClass.train(df)
        except Exception as e:
            print(e)
            days,hours,userID = 1,10,1
        dg = DateGenP()
        test = dg.date_df(int(days)*24 + int(hours), int(userID))
        test = test.rename(columns = {'Time': 'ds'})
        preds = ProphetClass.predict(test)
        #print(preds)
        response = preds
        # response.index = response['Time']
        print(response.to_csv(index=False))
        return response.to_csv(index=False)

# RNN

@app.route('/rnn/train',methods=['POST'])
def rnn_train():
    file = request.files['file']
    userID = int(request.form['userID'])
    df = pd.read_csv(file)    
    df = Rnn.preprocess(df,userID)
    Rnn.train(df)
    return "Model Trained Successfully" 

@app.route('/rnn/predict',methods=['POST'])
def rnn_predict():
    days = request.json['body']['days']
    hours = request.json['body']['hours']
    userID = request.json['body']['userID']
    #file = request.files['file']
    df = pd.read_csv('RNN_Predict.csv')
    hrs=int(days)*24 + int(hours)
    df = Rnn.preprocess(df,int(userID))
    preds = Rnn.predict(df,hrs)   
    response=preds
    print("response",response)
    return response.to_csv(index=False)   

# ML Models

@app.route('/mlmodels',methods=['POST'])
def MLModels():
    file = request.files['file'] 
    df = pd.read_csv(file)
    preds = MLModelsClass.model(df)
    print(preds)
    response = preds
    return response.to_csv()

# @app.route('/linearRegression',methods=['POST'])
# def linearRegression():
#     file = request.files['file'] 
#     df = pd.read_csv(file)
#     preds = linearRegressionClass.model(df)
#     print(preds)
#     response = preds
#     return response.to_csv()     

# @app.route('/randomForest',methods=['POST'])
# def randomForest():
#     file = request.files['file'] 
#     df = pd.read_csv(file)
#     preds = randomForestClass.model(df)
#     print(preds)
#     response = preds
#     return response.to_csv()       

# @app.route('/XGB',methods=['POST'])
# def XGB():
#     file = request.files['file'] 
#     df = pd.read_csv(file)
#     preds = XGBClass.model(df)
#     print(preds)
#     response = preds

# @app.route('/MultinomialNaiveBayes',methods=['POST'])
# def MultinomialNaiveBayes():
#     file = request.files['file'] 
#     df = pd.read_csv(file)
#     preds = MultinomialNaiveBayesClass.model(df)
#     print(preds)
#     response = preds    

# @app.route('/dateGen',methods=['GET'])
# def dategenerator():
#     df = DateGen.date_df(5,1)
#     response = df
#     return response.to_csv()


@app.route('/liststorages')
def list_storages():
    return{
        'resultStatus': 'SUCCESS',
        'message': ','.join(STORAGES_LIST)
    }

