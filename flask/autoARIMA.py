import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle

class AutoArima:
    def __init__(csv):
        pass
    
    def preprocess(df):
        dataset = df
        # df_User1 = dataset[dataset['UserID']==1]
        # df_User1.index = df_User1['Time']
        # df = df_User1.drop(['Time','UserID'],axis=1)
        
        # df_User1 = dataset[dataset['UserID']==1]
        dataset.index = dataset['Time']
        dataset = dataset[dataset["UserID"]==1]         
        # df = dataset.drop(['Time','UserID'],axis=1)
        df = dataset.drop(['Time'],axis=1)

        print(df)
        return df

    def train(df):
        test_size = 50
        test_ind = len(df) - test_size
        train = df.iloc[:test_ind]
        test = df.iloc[test_ind:]
        from pmdarima.arima import auto_arima
        arima_model = auto_arima(train, start_p=0, d=1, start_q=0,
        max_p=5, max_d=5, max_q=5, start_P=0,
        D=1, start_Q=0, max_P=5, max_D=5,
        max_Q=5, m=12, seasonal=True,
        error_action='warn',trace = True,
        supress_warnings=True, stepwise = True,
        random_state=20,n_fits = 50)
        arima_model.summary()
        with open('arima.pkl', 'wb') as pkl:
            pickle.dump(arima_model, pkl)
        return test
    
    def predict(test):
        test_size = len(test)
        with open('arima.pkl', 'rb') as pkl:
            prediction = pd.DataFrame(pickle.load(pkl).predict(n_periods=test_size),index=test.index)
            prediction.columns = ['forecast']
            print(prediction)
            return prediction

    def update(df):
        with open('arima.pkl', 'rb') as pkl:
            arima_model = pickle.load(pkl).update(df)
            pickle.dump(arima_model, pkl)