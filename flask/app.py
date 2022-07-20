from operator import index
import time
import os
import json
from urllib import request
import pandas as pd
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
from flask import Flask, flash, request, redirect, url_for, session, Response
from flask_cors import CORS
from flasgger import Swagger

UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

STORAGES_LIST = ['Storage 1', 'Storage 2', 'Storage 3', 'Storage 4']

app = Flask(__name__)
swagger = Swagger(app)
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
    """Test Endpoint to check if the flask server is running
    ---

    responses:
      200:
        description: Server Running
        schema:
          type: object
          properties:
            resultStatus:
              type: string
            message:
              type: string
          examples:
            resultStatus: SUCCESS
            message: Flask Running
    """
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
    """ Streaming from storage simulation
    ---

    responses:
      200:
        description: Server Running
        schema:
          type: object
          properties:
            resultStatus:
              type: string
            message:
              type: string
          examples:
            resultStatus: SUCCESS
            message: Flask Running
    """
    df = pd.read_csv("storage_train.csv")
    aa = AutoArima()
    df_prep = aa.preprocess(df,1)
    dg = DateGen()
    aa.train(df_prep[:50],1)
    def getdata():
        # file = request.files['file'] 
        
        for i in range(50,len(df_prep)):
            aa.update(df_prep[i:i+1], 1)
            df = dg.date_df(5,1,df_prep.index[i])
            preds = aa.predict(df,1)
            final_df = df_prep[49:i].append(preds)
            s = final_df.to_csv().replace('\r\n', '$')
            #gotcha
            yield f'data: {s} \n\n' 
            time.sleep(5)
            
    response = Response(getdata(), mimetype='text/event-stream')

    response.headers['Content-Disposition'] = 'inline'
    # response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    return response

# AutoArima

@app.route('/autoarima/train',methods=['POST'])
def autoarima_train():
    """Training Auto-ARIMA model with Storage dataset  
    ---
    consumes:
      - "multipart/form-data"
    produces:
      - "string"
    parameters:
      - in: formData
        name: file
        description: Storage dataset
        required: true
        type: file
      - in: formData
        name: userID
        description: User ID
        required: true
        type: integer
    responses:
      200:
        description: Status
        schema:
          type: string
        examples:
          result: Model Trained Successfully
          
    """
    aa = AutoArima()
    file = request.files['file']
    userID = int(request.form['userID'])
    df = pd.read_csv(file)
    df = aa.preprocess(df,userID)
    r2_score = aa.train(df, userID)
    return json.dumps({"message":"Model Trained Successfully", "R2":r2_score})

@app.route('/autoarima/update',methods=['POST'])
def autoarima_update():
    """ Updating Auto-ARIMA model with new data  
    ---
    consumes:
      - "multipart/form-data"
    produces:
      - "string"
    parameters:
      - in: formData
        name: file
        description: Storage dataset
        required: true
        type: file
      - in: formData
        name: userID
        description: User ID
        required: true
        type: integer
    responses:
      200:
        description: Status
        schema:
          type: string
        examples:
          result: Updated Model Successfully
          
    """
    aa = AutoArima()
    file = request.files['file'] 
    userID = int(request.form['userID'])
    df = pd.read_csv(file)
    df = aa.preprocess(df,userID)
    aa.update(df, userID)
    return "Updated Model Successfully"

@app.route('/autoarima/predict',methods=['POST'])
def autoarima_predict():
    """ Future Predictions 
    ---
    consumes:
      - "application/json"
    produces:
      - "application/json"
    parameters:
      - in: "body"
        name: "body"
        description: "Accepts a input dictionary of Time and User ID"
        required: true
        schema:
          type: object
          properties:
            body:
              type: object
              properties:
                days:
                  type: integer
                hours:
                  type: integer
                userID:
                  type: string
        example: {"days": 2,"hours":5,"userID": 1}
    responses:
      200:
        description: Status
        schema:
          type: object
        examples:
          result: Model Trained Successfully
    """
    aa = AutoArima()
    days = request.json['body']['days']
    hours = request.json['body']['hours']
    userID = request.json['body']['userID']
    dg = DateGen()
    fil = open('arima' + str(userID) + '.txt','r')
    df = dg.date_df(int(days)*24 + int(hours), int(userID),fil.readline().strip())
    fil.close()
    preds = aa.predict(df, userID)
    response=preds
    return response.to_csv()

# Linear Regression

@app.route('/linearRegression/train',methods=['POST'])
def linearRegression_train():
    """ Training Linear Regression model with Storage dataset  
    ---
    consumes:
      - "multipart/form-data"
    produces:
      - "string"
    parameters:
      - in: formData
        name: file
        description: Storage dataset
        required: true
        type: file
      - in: formData
        name: userID
        description: User ID
        required: true
        type: integer
    responses:
      200:
        description: Status
        schema:
          type: string
        examples:
          result: Model Trained Successfully
    """
    file = request.files['file']
    userID = int(request.form['userID'])
    df = pd.read_csv(file)    
    df = linearRegressionClass.preprocess(df,userID,"train")
    r2_score = linearRegressionClass.train(df, userID)     
    return json.dumps({"message":"Model Trained Successfully", "R2":r2_score})  

@app.route('/linearRegression/predict',methods=['POST'])
def linearRegression_predict():
    """ Future Predictions 
      ---
      consumes:
        - "application/json"
      produces:
        - "application/json"
      parameters:
        - in: "body"
          name: "body"
          description: "Accepts a input dictionary of Time and User ID"
          required: true
          schema:
            type: object
            properties:
              body:
                type: object
                properties:
                  days:
                    type: integer
                  hours:
                    type: integer
                  userID:
                    type: string
          example: {"days": 2,"hours":5,"userID": 1}
      responses:
        200:
          description: Status
          schema:
            type: object
            properties:
              days:
                type: integer
              hours:
                type: integer
              userID:
                type: string
          examples:
            result: {"days": 2,"hours":5,"userID": 1}
      """
    days = request.json['body']['days']
    hours = request.json['body']['hours']
    userID = request.json['body']['userID']
  
    df = pd.read_csv('LR_Predict.csv')
    hrs=int(days)*24 + int(hours)
    df = linearRegressionClass.preprocess(df,int(userID),"predict")
    preds = linearRegressionClass.predict(df,hrs,userID)    
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
    """ Training RNN model with Storage dataset  
      ---
      consumes:
        - "multipart/form-data"
      produces:
        - "string"
      parameters:
        - in: formData
          name: file
          description: Storage dataset
          required: true
          type: file
        - in: formData
          name: userID
          description: User ID
          required: true
          type: integer
      responses:
        200:
          description: Status
          schema:
            type: string
          examples:
            result: Model Trained Successfully
      """
    file = request.files['file']
    userID = int(request.form['userID'])
    df = pd.read_csv(file)    
    df = Rnn.preprocess(df,userID,"train")    
    r2_score = Rnn.train(df,userID)  
    return json.dumps({"message":"Model Trained Successfully", "R2":r2_score})  


@app.route('/rnn/predict',methods=['POST'])
def rnn_predict():
    """ Future Predictions 
        ---
        consumes:
          - "application/json"
        produces:
          - "application/json"
        parameters:
          - in: "body"
            name: "body"
            description: "Accepts a input dictionary of Time and User ID"
            required: true
            schema:
              type: object
              properties:
                body:
                  type: object
                  properties:
                    days:
                      type: integer
                    hours:
                      type: integer
                    userID:
                      type: string
            example: {"days": 2,"hours":5,"userID": 1}
        responses:
          200:
            description: Status
            schema:
              type: object
              properties:
                days:
                  type: integer
                hours:
                  type: integer
                userID:
                  type: string
            examples:
              result: {"days": 2,"hours":5,"userID": 1}
        """
    days = request.json['body']['days']
    hours = request.json['body']['hours']
    userID = request.json['body']['userID']

    df = pd.read_csv('RNN_Predict.csv')
    hrs=int(days)*24 + int(hours)
    df = Rnn.preprocess(df,int(userID),"predict")    
    preds = Rnn.predict(df,hrs,userID)  
    response=preds    
    return response.to_csv(index=False)   
   

@app.route('/liststorages')
def list_storages():
    return{
        'resultStatus': 'SUCCESS',
        'message': ','.join(STORAGES_LIST)
    }

