import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,LSTM,SimpleRNN
from tensorflow.keras.models import load_model
# from sklearn.metrics import mean_squared_error
# from math import sqrt

class Rnn:
    def __init__():
        pass 

    def preprocess(df,UserID,status):  
      if(status=="train"):
          df = df[df["UserID"]==UserID] 
          df[:].to_csv('RNN_Predict.csv',index=False)

      #df.index = df['Time']
      try:
          df = df[df["UserID"]==UserID]
          df.index = df['Time']
          df = df.drop(['Time','UserID'],axis=1)
      except:
          df = df.drop(['Time'],axis=1)
          print("no UserID Col")
      print(df.head())
      #769 as 31 days + 24 hours
      if(status=="train"):
          #df[-769:].to_csv('RNN_Predict.csv',index=False)
          return df[:-769] 
      elif(status=="predict"):
          return df         

    def train(df,userID):       
      test_point = -769      
      train = df.iloc[:test_point]
      test = df.iloc[test_point:]
      scaler = MinMaxScaler()
      scaler.fit(train)
      scaled_train = scaler.transform(train)
      scaled_test = scaler.transform(test)
      length = 18 # Length of the output sequences (in number of timesteps)
      batch_size = 1 #Number of timeseries samples in each batch
      generator = TimeseriesGenerator(scaled_train, scaled_train, length=length, batch_size=batch_size)
      #X,y = generator[0]     
      n_features = 1
      # define model
      model = Sequential()
      # Simple RNN layer
      model.add(SimpleRNN(18,input_shape=(length, n_features)))
      # Final Prediction
      model.add(Dense(1))
      model.compile(optimizer='adam', loss='mse')
      model.fit_generator(generator,epochs=5)
      model.save('RNN'+ str(userID) +'.h5')
      print("model saved")    
      
    def predict(df,hrs,userID): 
      test_point = -769      
      train = df.iloc[:test_point]
      test = df.iloc[test_point:test_point+hrs]
      scaler = MinMaxScaler()
      scaler.fit(train)
      scaled_train = scaler.transform(train)
      scaled_test = scaler.transform(test)
      length = 18 # Length of the output sequences (in number of timesteps)
      batch_size = 1 #Number of timeseries samples in each batch   
      n_features = 1
      model = load_model('RNN'+ str(userID) +'.h5')
      # summarize model.
      model.summary()
      test_predictions = []
      first_eval_batch = scaled_train[-length:]
      current_batch = first_eval_batch.reshape((1, length, n_features))
      for i in range(len(test)):          
          # get prediction 1 time stamp ahead ([0] is for grabbing just the number instead of [array])
          current_pred = model.predict(current_batch)[0]          
          # store prediction
          test_predictions.append(current_pred)           
          # update batch to now include prediction and drop first value
          current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)
         
      true_predictions = scaler.inverse_transform(test_predictions)    
      test['Predictions'] = true_predictions
      test['Time']=test.index
      test.reset_index(drop=True, inplace=True)
      print(test)              
      return test[['Time','Predictions']]
        