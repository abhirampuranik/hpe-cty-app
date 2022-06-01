import pandas as pd

class MLModelsClass:
    def __init__():
        pass 

    def model(dataset):
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

        from sklearn.linear_model import LinearRegression
        lin_model=LinearRegression()

        from sklearn.ensemble import RandomForestRegressor
        model=RandomForestRegressor(n_estimators=100,max_features=3, random_state=1)

        import xgboost as xgb
        xgb_model=xgb.XGBRegressor()

        from sklearn.naive_bayes import MultinomialNB
        multi_model = MultinomialNB()

        import numpy as np
        x1,x2,x3,y=df['Usage_LastMonth'],df['Usage_2Monthsback'],df['Usage_3Monthsback'],df['Usage']
        x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
        x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
        final_x=np.concatenate((x1,x2,x3),axis=1)
        #print(final_x)

        test_ind = len(df) - 30
        train = df.iloc[:test_ind]
        test = df.iloc[test_ind:]
        X_train,X_test,y_train,y_test=final_x[:-30],final_x[-30:],y[:-30],y[-30:]

        model.fit(X_train,y_train)
        lin_model.fit(X_train,y_train)
        xgb_model.fit(X_train,y_train)
        multi_model.fit(X_train,y_train)

        pred=model.predict(X_test)
        print("Random_Forest_Predictions")
        test['Random_Forest_Predictions']=pred
        # print(pred)
        # import matplotlib.pyplot as plt
        # plt.rcParams["figure.figsize"] = (11,6)
        # plt.plot(pred,label='Random_Forest_Predictions')
        # plt.plot(y_test,label='Actual Usage')
        # plt.legend(loc="upper left")
        # plt.show()

        lin_pred=lin_model.predict(X_test)
        print("Linear_Regression_Predictions")
        test['Linear_Regression_Predictions']=lin_pred
        # print(lin_pred)
        # import matplotlib.pyplot as plt
        # plt.rcParams["figure.figsize"] = (11,6)
        # plt.plot(lin_pred,label='Linear_Regression_Predictions')
        # plt.plot(y_test,label='Actual Usage')
        # plt.legend(loc="upper left")
        # plt.show()

        xgb_pred=xgb_model.predict(X_test)
        print("Extreme_Gradient_Booster")
        test['Extreme_Gradient_Booster']=xgb_pred
        # print(xgb_pred)
        # import matplotlib.pyplot as plt
        # plt.rcParams["figure.figsize"] = (11,6)
        # plt.plot(xgb_pred,label='Extreme_Gradient_Booster')
        # plt.plot(y_test,label='Actual Usage')
        # plt.legend(loc="upper left")
        # plt.show()

        multi_pred=multi_model.predict(X_test)
        print("Mulinomial_Naive_Bayes")
        test['Mulinomial_Naive_Bayes']=multi_pred
        # print(multi_pred)
        # import matplotlib.pyplot as plt
        # plt.rcParams["figure.figsize"] = (11,6)
        # plt.plot(multi_pred,label='Mulinomial_Naive_Bayes')
        # plt.plot(y_test,label='Actual Usage')
        # plt.legend(loc="upper left")
        # plt.show()

        return test
