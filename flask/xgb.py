import pandas as pd
import pickle

class XGBClass:
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
        import xgboost as xgb
        xgb_model=xgb.XGBRegressor()
        
        import numpy as np
        x1,x2,x3,y=df['Usage_LastMonth'],df['Usage_2Monthsback'],df['Usage_3Monthsback'],df['Usage']
        x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
        x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
        final_x=np.concatenate((x1,x2,x3),axis=1)

        test_ind = len(df) - 30
        train = df.iloc[:test_ind]
        test = df.iloc[test_ind:]
        X_train,X_test,y_train,y_test=final_x[:-30],final_x[-30:],y[:-30],y[-30:]

        xgb_model.fit(X_train,y_train) 
        with open('xgb.pkl', 'wb') as pkl:
            pickle.dump(xgb_model, pkl)
        return X_test     

    def predict(test):
        test_size = len(test)
        with open('xgb.pkl', 'rb') as pkl:
            prediction = pd.DataFrame(pickle.load(pkl).predict(n_periods=test_size),index=test.index)
            prediction.columns = ['forecast']
            print(prediction)
            return prediction

    def update(df):
        with open('xgb.pkl', 'rb') as pkl:
            xgb_model = pickle.load(pkl).update(df)
            with open('xgb.pkl', 'wb') as pkl:
                pickle.dump(xgb_model, pkl)    

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

    #     import xgboost as xgb
    #     xgb_model=xgb.XGBRegressor()

    #     import numpy as np
    #     x1,x2,x3,y=df['Usage_LastMonth'],df['Usage_2Monthsback'],df['Usage_3Monthsback'],df['Usage']
    #     x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
    #     x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
    #     final_x=np.concatenate((x1,x2,x3),axis=1)

    #     test_ind = len(df) - 30
    #     train = df.iloc[:test_ind]
    #     test = df.iloc[test_ind:]
    #     X_train,X_test,y_train,y_test=final_x[:-30],final_x[-30:],y[:-30],y[-30:]
       
    #     xgb_model.fit(X_train,y_train)

        # XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
        #       colsample_bynode=1, colsample_bytree=1, gamma=0, gpu_id=-1,
        #       importance_type='gain', interaction_constraints='',
        #       learning_rate=0.300000012, max_delta_step=0, max_depth=6,
        #       min_child_weight=1, missing=nan, monotone_constraints='()',
        #       n_estimators=100, n_jobs=0, num_parallel_tree=1,
        #       objective='multi:softprob', random_state=0, reg_alpha=0,
        #       reg_lambda=1, scale_pos_weight=None, subsample=1,
        #       tree_method='exact', validate_parameters=1, verbosity=None)

        # pickle.dump(xgb_model, open('xgb.pkl', 'wb'))
        # pickled_model = pickle.load(open('xbg.pkl', 'rb'))
        # pickled_model.predict(X_test)

        # xgb_pred=xgb_model.predict(X_test)
        # print("Extreme_Gradient_Booster")
        # test['Extreme_Gradient_Booster']=xgb_pred       

        # return test
