import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle

class AutoArima:
    def __init__(csv):
        pass
    
    def preprocess(df,UserID):
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        # df_User1 = df[df['UserID']==1]
        # df_User1.index = df_User1['Time']
        # df = df_User1.drop(['Time','UserID'],axis=1)
        
        # df_User1 = df[df['UserID']==1]
        # print(UserID)
        df.index = df['Time']
        try:
            df = df[df["UserID"]==UserID]
            df = df.drop(['Time','UserID'],axis=1)
        except:
            df = df.drop(['Time'],axis=1)
            print("no UserID Col")
        print(df)
        return df

    def train(df):
        train = df
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
            with open('arima.pkl', 'wb') as pkl:
                pickle.dump(arima_model, pkl)

# df = pd.read_csv('../test_data/storage.csv')
# df = AutoArima.preprocess(df,1)
# test = df[:-50]
# test = AutoArima.train(test[:25])
# update = AutoArima.update(df[25:])