import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.naive_bayes import MultinomialNB
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from math import sqrt
lin_model=LinearRegression()       
model=RandomForestRegressor(n_estimators=100,max_features=3, random_state=1)        
xgb_model=xgb.XGBRegressor()       
multi_model = MultinomialNB()
# df=pd.DataFrame()

class ML_Models:
    def __init__():
        pass

    def preprocess(df):              
        df = pd.read_csv(df,index_col='Time',parse_dates=True)
        df.index.freq = 'MS' 
        df.columns = ['Usage']
        df['Usage_LastMonth']=df['Usage'].shift(+1)
        df['Usage_2Monthsback']=df['Usage'].shift(+2)
        df['Usage_3Monthsback']=df['Usage'].shift(+3)
        df=df.dropna()    
        print(df)
        return df

    def train(df):        
        lin_model=LinearRegression()       
        # model=RandomForestRegressor(n_estimators=100,max_features=3, random_state=1)        
        # xgb_model=xgb.XGBRegressor()       
        # multi_model = MultinomialNB()
        x1,x2,x3,y=df['Usage_LastMonth'],df['Usage_2Monthsback'],df['Usage_3Monthsback'],df['Usage']
        x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
        x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
        final_x=np.concatenate((x1,x2,x3),axis=1)
        #print(final_x)

        X_train,X_test,y_train,y_test=final_x[:-30],final_x[-30:],y[:-30],y[-30:]
        test = [X_test,y_test]
        
        # return final_x 
        with open('linear.pkl', 'wb') as pkl:
            pickle.dump(lin_model, pkl)
        return test    
          

    def predict(test):
        
        X_train,y_train=test
        model.fit(X_train,y_train)
        # lin_model.fit(X_train,y_train)
        # xgb_model.fit(X_train,y_train)
        # multi_model.fit(X_train,y_train)

        with open('randomForest.pkl', 'wb') as pkl:
            pickle.dump(model, pkl)
        return test 

        pred=model.predict(X_test)
        lin_pred=lin_model.predict(X_test)
        xgb_pred=xgb_model.predict(X_test)
        multi_pred=multi_model.predict(X_test)
        
        with open('linear.pkl', 'rb') as pkl:
            prediction = pd.DataFrame(pickle.load(pkl).predict(n_periods=test_size),index=test.index)
            prediction.columns = ['forecast']
            print(prediction)
            return prediction    

       

        
        with open('arima.pkl', 'wb') as pkl:
            pickle.dump(arima_model, pkl)
        return test    

# df = pd.read_csv('/content/Random.csv',index_col='Time',parse_dates=True)
# df.index.freq = 'MS'

# df.tail()

# df.columns = ['Usage']
# df.plot(figsize=(12,8))

# df['Usage_LastMonth']=df['Usage'].shift(+1)
# df['Usage_2Monthsback']=df['Usage'].shift(+2)
# df['Usage_3Monthsback']=df['Usage'].shift(+3)
# df

# df=df.dropna()
# df

# from sklearn.linear_model import LinearRegression
# lin_model=LinearRegression()

# from sklearn.ensemble import RandomForestRegressor
# model=RandomForestRegressor(n_estimators=100,max_features=3, random_state=1)

# import xgboost as xgb
# xgb_model=xgb.XGBRegressor()

# from sklearn.naive_bayes import MultinomialNB
# multi_model = MultinomialNB()

# import numpy as np
# x1,x2,x3,y=df['Usage_LastMonth'],df['Usage_2Monthsback'],df['Usage_3Monthsback'],df['Usage']
# x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
# x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
# final_x=np.concatenate((x1,x2,x3),axis=1)
# print(final_x)





# plt.rcParams["figure.figsize"] = (11,6)
# plt.plot(pred,label='Random_Forest_Predictions')
# plt.plot(y_test,label='Actual Usage')
# plt.legend(loc="upper left")
# plt.show()


# plt.rcParams["figure.figsize"] = (11,6)
# plt.plot(lin_pred,label='Linear_Regression_Predictions')
# plt.plot(y_test,label='Actual Usage')
# plt.legend(loc="upper left")
# plt.show()



# plt.rcParams["figure.figsize"] = (11,6)
# plt.plot(xgb_pred,label='Extreme_Gradient_Booster')
# plt.plot(y_test,label='Actual Usage')
# plt.legend(loc="upper left")
# plt.show()



# plt.rcParams["figure.figsize"] = (11,6)
# plt.plot(multi_pred,label='Mulinomial_Naive_Bayes')
# plt.plot(y_test,label='Actual Usage')
# plt.legend(loc="upper left")
# plt.show()


# rmse_rf=sqrt(mean_squared_error(pred,y_test))
# rmse_lr=sqrt(mean_squared_error(lin_pred,y_test))
# rmse_xgb=sqrt(mean_squared_error(xgb_pred,y_test))
# rmse_multi=sqrt(mean_squared_error(multi_pred,y_test))

# print('Mean Squared Error for Random Forest Model is:',rmse_rf)
# print('Mean Squared Error for Linear Regression Model is:',rmse_lr)
# print('Mean Squared Error for Extreme_Gradient_Booster is:',rmse_xgb)
# print('Mean Squared Error for Mulinomial_Naive_Bayes is:',rmse_multi)