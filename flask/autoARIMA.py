from pickletools import read_uint1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from sklearn.metrics import r2_score, mean_squared_error
from pmdarima.arima import auto_arima
# test['predicted sales'] = prediction
# r2_score(test[' Champagne sales'], test['predicted sales'])
class AutoArima:
    def __init__(self):
        pass
    
    def preprocess(self,df,UserID):
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.index = df['Time']
        try:
            df = df[df["UserID"]==UserID]
            df = df.drop(['Time','UserID'],axis=1)
        except:
            df = df.drop(['Time'],axis=1)
            print("no UserID Col")
        return df

    def train(self,df, userID):
        test_size = int(len(df)*0.2)
        test_ind = len(df)- test_size
        train = df.iloc[:test_ind]
        test = df.iloc[test_ind:]
        # train = df
        arima_model = auto_arima(train, start_p=0, d=1, start_q=0,
        max_p=5, max_d=5, max_q=5, start_P=0,
        D=1, start_Q=0, max_P=5, max_D=5,
        max_Q=5, m=12, seasonal=True,
        error_action='warn',trace = True,
        supress_warnings=True, stepwise = True,
        random_state=20,n_fits = 50)
        arima_model.summary()
        with open('arima' + str(userID) + '.pkl', 'wb') as pkl:
            pickle.dump(arima_model, pkl)
        last_date = train.index[-1]
        with open('arima' + str(userID) + '.txt','w') as fil:
            fil.write(last_date)
        prediction = self.predict(test,userID)
        self.update(test,userID)
        test['predicted Usage'] = prediction
        acc = r2_score(test['Usage'], test['predicted Usage'])
        print(acc)
        return acc

    def predict(self,test, userID):
        test_size = len(test)
        with open('arima' + str(userID) + '.pkl', 'rb') as pkl:
            prediction = pd.DataFrame(pickle.load(pkl).predict(n_periods=test_size),index=test.index)
            prediction.columns = ['Usage']
            return prediction

    def update(self,df, userID):
        with open('arima' + str(userID) + '.pkl', 'rb') as pkl:
            arima_model = pickle.load(pkl).update(df)
            with open('arima' + str(userID) + '.pkl', 'wb') as pkl:
                pickle.dump(arima_model, pkl)
        last_date = df.index[-1]
        with open('arima' + str(userID) + '.txt','w') as fil:
            fil.write(last_date)