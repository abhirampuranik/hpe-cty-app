import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator

dataset = pd.read_csv('../test_data/Seasonal.csv')
df = dataset 
df.index = df['Time']
df = df.drop(['Time'],axis=1)
test_percent = 0.1
len(df)*test_percent
test_point = np.round(len(df)*test_percent)
test_ind = int(len(df) - test_point)
train = df.iloc[:test_ind]
test = df.iloc[test_ind:]
scaler = MinMaxScaler()
scaler.fit(train)
scaled_train = scaler.transform(train)
scaled_test = scaler.transform(test)
length = 18 # Length of the output sequences (in number of timesteps)
batch_size = 1 #Number of timeseries samples in each batch
generator = TimeseriesGenerator(scaled_train, scaled_train, length=length, batch_size=batch_size)
X,y = generator[0]

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,LSTM,SimpleRNN
n_features = 1
# define model
model = Sequential()

# Simple RNN layer
model.add(SimpleRNN(18,input_shape=(length, n_features)))

# Final Prediction
model.add(Dense(1))

model.compile(optimizer='adam', loss='mse')

model.fit_generator(generator,epochs=5)

first_eval_batch = scaled_train[-length:]

first_eval_batch

first_eval_batch = first_eval_batch.reshape((1, length, n_features))

model.predict(first_eval_batch)

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

    # IGNORE WARNINGS
test['Predictions'] = true_predictions
from tensorflow.keras.callbacks import EarlyStopping

early_stop = EarlyStopping(monitor='val_loss',patience=2)

length = 12

generator = TimeseriesGenerator(scaled_train,scaled_train,
                               length=length,batch_size=1)

validation_generator = TimeseriesGenerator(scaled_test,scaled_test,length=length,batch_size=1)



model = Sequential()

# Simple RNN layer
model.add(LSTM(20,input_shape=(length, n_features)))

# Final Prediction
model.add(Dense(1))

model.compile(optimizer='adam', loss='mse')

model.fit_generator(generator,epochs=20,
                   validation_data=validation_generator,
                   callbacks=[early_stop])


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
test['LSTM Predictions'] = true_predictions

test.plot(figsize=(12,8))
