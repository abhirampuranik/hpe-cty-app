import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pickle
# from sklearn.metrics import mean_squared_error
# from math import sqrt

class linearRegressionClass:
	def __init__():
		pass 

	def preprocess(df,UserID):		 
		df.index = df['Time']
		df['Usage_LastHour']=df['Usage'].shift(+1)
		df['Usage_2Hoursback']=df['Usage'].shift(+2)
		df['Usage_3Hoursback']=df['Usage'].shift(+3)
		df=df.dropna()
		try:
 			df = df[df["UserID"]==UserID]
 			df = df.drop(['Time','UserID'],axis=1)
		except:
 			df = df.drop(['Time'],axis=1)
 			print("no UserID Col")     
		print(df.head())
		return df

	def train(df):  	
		lin_model=LinearRegression()		
		x1,x2,x3,y=df['Usage_LastHour'],df['Usage_2Hoursback'],df['Usage_3Hoursback'],df['Usage']
		x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
		x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
		final_x=np.concatenate((x1,x2,x3),axis=1)		
		train = df.iloc[:-120]
		X_train,y_train=final_x[:-120],y[:-120]		
		lin_model.fit(X_train,y_train) 
		with open('LinearRegression.pkl', 'wb') as pkl:
			pickle.dump(lin_model, pkl)
		
	def predict(df,hrs):
		#lin_model=LinearRegression()
		x1,x2,x3,y=df['Usage_LastHour'],df['Usage_2Hoursback'],df['Usage_3Hoursback'],df['Usage']
		x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
		x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
		final_x=np.concatenate((x1,x2,x3),axis=1)	
		train = df.iloc[:-120]
		test = df.iloc[-120:-120+hrs]		
		X_train,X_test,y_train,y_test=final_x[:-120],final_x[-120:-120+hrs],y[:-120],y[-120:-120+hrs]
		#lin_model.fit(X_train,y_train) 
		with open('LinearRegression.pkl', 'rb') as pkl:
			#prediction = pd.DataFrame(pickle.load(pkl).predict(X_test))
			prediction = pickle.load(pkl).predict(X_test)
			# print(prediction)
			#lin_pred=lin_model.predict(X_test)
			print("Linear_Regression_Predictions")
			test['Linear_Regression_Predictions']=prediction

			test['Time']=test.index
			test.reset_index(drop=True, inplace=True)
			print(test[['Time','Linear_Regression_Predictions']])
			return test[['Time','Linear_Regression_Predictions']]
			
	def update(df):
		#lin_model=LinearRegression()
		x1,x2,x3,y=df['Usage_LastHour'],df['Usage_2Hoursback'],df['Usage_3Hoursback'],df['Usage']
		x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
		x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
		final_x=np.concatenate((x1,x2,x3),axis=1)	
		train = df.iloc[:-120]
		test = df.iloc[-120:-120+hrs]		
		X_train,X_test,y_train,y_test=final_x[:-120],final_x[-120:-120+hrs],y[:-120],y[-120:-120+hrs]

		X_train,X_test,y_train,y_test=final_x,final_x,y,y
		lin_model.fit(X_test,y_test)

		# with open('LinearRegression.pkl', 'wb') as out:
		# 	pickle.dump(lin_model, out)
		
		with open('LinearRegression.pkl', 'rb') as inp:	
			linear_model=pickle.load(inp)			 
			with open('LinearRegression1.pkl', 'wb') as out:
				pickle.dump(linear_model, out)
				pickle.dump(lin_model, out)

		# with open('LinearRegression.pkl', 'rb') as pkl:
		# 	#prediction = pd.DataFrame(pickle.load(pkl).predict(n_periods=test_size),index=test.index)
		# 	prediction = pd.DataFrame(pickle.load(pkl).predict(X_test))
		# 	#lin_pred=lin_model.predict(X_test)
  #   		#print("Linear_Regression_Predictions")
  #   		#test['Linear_Regression_Predictions']=lin_pred
		# 	prediction.columns = ['Usage']

		
		

		# with open('LinearRegression.pkl', 'rb') as pkl:
		# 	# linear_model = pickle.load(pkl).update(df)
		# 	linear_model = pickle.load(pkl)
		# 	with open('LinearRegression.pkl', 'wb') as pkl:
		# 		pickle.dump(linear_model, pkl)        
        
   #      with open('LinearRegression.pkl', 'wb') as pkl:
			# pickle.dump(linear_model, pkl)  

			
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

    #     from sklearn.linear_model import LinearRegression
    #     lin_model=LinearRegression()

    #     import numpy as np
    #     x1,x2,x3,y=df['Usage_LastMonth'],df['Usage_2Monthsback'],df['Usage_3Monthsback'],df['Usage']
    #     x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
    #     x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
    #     final_x=np.concatenate((x1,x2,x3),axis=1)

    #     test_ind = len(df) - 30
    #     train = df.iloc[:test_ind]
    #     test = df.iloc[test_ind:]
    #     X_train,X_test,y_train,y_test=final_x[:-30],final_x[-30:],y[:-30],y[-30:]

    #     lin_model.fit(X_train,y_train)  
        
    #     lin_pred=lin_model.predict(X_test)
    #     print("Linear_Regression_Predictions")
    #     test['Linear_Regression_Predictions']=lin_pred       

    #     return test
