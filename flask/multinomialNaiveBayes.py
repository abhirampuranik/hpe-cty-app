import pandas as pd
import pickle

class MultinomialNaiveBayesClass:
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
        from sklearn.naive_bayes import MultinomialNB
        multi_model = MultinomialNB()
        
        import numpy as np
        x1,x2,x3,y=df['Usage_LastMonth'],df['Usage_2Monthsback'],df['Usage_3Monthsback'],df['Usage']
        x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
        x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
        final_x=np.concatenate((x1,x2,x3),axis=1)

        test_ind = len(df) - 30
        train = df.iloc[:test_ind]
        test = df.iloc[test_ind:]
        X_train,X_test,y_train,y_test=final_x[:-30],final_x[-30:],y[:-30],y[-30:]

        multi_model.fit(X_train,y_train) 
        with open('MNB.pkl', 'wb') as pkl:
            pickle.dump(multi_model, pkl)
        return X_test     

    def predict(test):
        test_size = len(test)
        with open('MNB.pkl', 'rb') as pkl:
            prediction = pd.DataFrame(pickle.load(pkl).predict(n_periods=test_size),index=test.index)
            prediction.columns = ['forecast']
            print(prediction)
            return prediction

    def update(df):
        with open('MNB.pkl', 'rb') as pkl:
            multi_model = pickle.load(pkl).update(df)
            with open('MNB.pkl', 'wb') as pkl:
                pickle.dump(multi_model, pkl)    

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

    #     from sklearn.naive_bayes import MultinomialNB
    #     multi_model = MultinomialNB()

    #     import numpy as np
    #     x1,x2,x3,y=df['Usage_LastMonth'],df['Usage_2Monthsback'],df['Usage_3Monthsback'],df['Usage']
    #     x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
    #     x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
    #     final_x=np.concatenate((x1,x2,x3),axis=1)
 
    #     test_ind = len(df) - 30
    #     train = df.iloc[:test_ind]
    #     test = df.iloc[test_ind:]
    #     X_train,X_test,y_train,y_test=final_x[:-30],final_x[-30:],y[:-30],y[-30:]
        
    #     multi_model.fit(X_train,y_train)       

    #     multi_pred=multi_model.predict(X_test)
    #     print("Multinomial_Naive_Bayes")
    #     test['Multinomial_Naive_Bayes']=multi_pred        

    #     return test
