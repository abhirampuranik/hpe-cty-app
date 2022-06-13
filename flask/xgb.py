import pandas as pd

class XGBClass:
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

        xgb_pred=xgb_model.predict(X_test)
        print("Extreme_Gradient_Booster")
        test['Extreme_Gradient_Booster']=xgb_pred       

        return test
