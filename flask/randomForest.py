import pandas as pd
import pickle

class randomForestClass:
    def __init__():
        pass 

    def preprocess(dataset):   
        # df=pd.DataFrame()
        # df = pd.read_csv(dataset,index_col='Time',parse_dates=True)
        df = dataset 
        df.index = df['Time']
        df.index.freq = 'MS'
        #df.tail()
        # df.columns = ['Usage']
        df.plot(figsize=(12,8))

        df['Usage_LastMonth']=df['Usage'].shift(+1)
        df['Usage_2Monthsback']=df['Usage'].shift(+2)
        df['Usage_3Monthsback']=df['Usage'].shift(+3)
        #df
        
        df=df.dropna()
        #df
        return df

    def train(df):    
        from sklearn.ensemble import RandomForestRegressor
        rf_model=RandomForestRegressor(n_estimators=100,max_features=3, random_state=1)
        
        import numpy as np
        x1,x2,x3,y=df['Usage_LastMonth'],df['Usage_2Monthsback'],df['Usage_3Monthsback'],df['Usage']
        x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
        x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
        final_x=np.concatenate((x1,x2,x3),axis=1)

        test_ind = len(df) - 30
        train = df.iloc[:test_ind]
        test = df.iloc[test_ind:]
        X_train,X_test,y_train,y_test=final_x[:-30],final_x[-30:],y[:-30],y[-30:]

        rf_model.fit(X_train,y_train) 
        with open('RandomForest.pkl', 'wb') as pkl:
            pickle.dump(rf_model, pkl)
        return X_test     

    def predict(test):
        test_size = len(test)
        with open('RandomForest.pkl', 'rb') as pkl:
            prediction = pd.DataFrame(pickle.load(pkl).predict(n_periods=test_size),index=test.index)
            prediction.columns = ['forecast']
            print(prediction)
            return prediction

    def update(df):
        with open('RandomForest.pkl', 'rb') as pkl:
            rf_model = pickle.load(pkl).update(df)
            with open('RandomForest.pkl', 'wb') as pkl:
                pickle.dump(rf_model, pkl)            
        
    # def model(dataset):
    #     # df=pd.DataFrame()
    #     # df = pd.read_csv(dataset,index_col='Time',parse_dates=True)
    #     df = dataset 
    #     df.index = df['Time']
    #     df.index.freq = 'MS'
    #     #df.tail()
    #     # df.columns = ['Usage']
    #     df.plot(figsize=(12,8))

    #     df['Usage_LastMonth']=df['Usage'].shift(+1)
    #     df['Usage_2Monthsback']=df['Usage'].shift(+2)
    #     df['Usage_3Monthsback']=df['Usage'].shift(+3)
    #     #df

    #     df=df.dropna()
    #     #df

    #     from sklearn.ensemble import RandomForestRegressor
    #     model=RandomForestRegressor(n_estimators=100,max_features=3, random_state=1)

    #     import numpy as np
    #     x1,x2,x3,y=df['Usage_LastMonth'],df['Usage_2Monthsback'],df['Usage_3Monthsback'],df['Usage']
    #     x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
    #     x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
    #     final_x=np.concatenate((x1,x2,x3),axis=1)
   
    #     test_ind = len(df) - 30
    #     train = df.iloc[:test_ind]
    #     test = df.iloc[test_ind:]
    #     X_train,X_test,y_train,y_test=final_x[:-30],final_x[-30:],y[:-30],y[-30:]

    #     model.fit(X_train,y_train)        

    #     pred=model.predict(X_test)
    #     print("Random_Forest_Predictions")
    #     test['Random_Forest_Predictions']=pred      

    #     return test
