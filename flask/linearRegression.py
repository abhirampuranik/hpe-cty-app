import pandas as pd
import numpy as np
from sklearn import tree, model_selection
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
# from sklearn.ensemble import RandomForestRegressor
# import xgboost as xgb
# from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt
import pickle
from sklearn.metrics import mean_squared_error
from math import sqrt
lin_model=LinearRegression()
# lin_model=RandomForestRegressor(n_estimators=100,max_features=3, random_state=1)
#lin_model=xgb.XGBRegressor()
#lin_model = MultinomialNB()
kfold = model_selection.KFold(n_splits=10)

class linearRegressionClass:
	def __init__():
		pass 

	def preprocess(df,UserID,status):
		if(status=="train"):
			df = df[df["UserID"]==UserID]	
			df[-772:].to_csv('LR_Predict.csv',index=False)	 

		try:
			df = df[df["UserID"]==UserID]
			df.index = df['Time']
			df['Usage_LastHour']=df['Usage'].shift(+1)
			df['Usage_2Hoursback']=df['Usage'].shift(+2)
			df['Usage_3Hoursback']=df['Usage'].shift(+3)
			df=df.dropna()
			df = df.drop(['Time','UserID'],axis=1)

		except:
			df = df.drop(['Time'],axis=1)
			print("no UserID Col")     
		print(df.head())
	    #769 as 31 days + 24 hours
		if(status=="train"):			
			return df[:-769]
		elif(status=="predict"):
			return df	

	def train(df,userID):  	
		# lin_model=LinearRegression()		
		x1,x2,x3,y=df['Usage_LastHour'],df['Usage_2Hoursback'],df['Usage_3Hoursback'],df['Usage']
		x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
		x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
		final_x=np.concatenate((x1,x2,x3),axis=1)		
		
		train=df
		
		X_train,y_train=final_x,y	
		lin_model.fit(X_train,y_train) 

		scoring = "neg_mean_absolute_error"
		results = model_selection.cross_val_score(lin_model, X_train, y_train, cv=kfold, scoring=scoring)
		# print("Mean Absolute Error: ", results.mean()) 
		# print("Standard Deviation: ", results.std())

		scoring = "neg_mean_squared_error"
		results = model_selection.cross_val_score(lin_model, X_train, y_train, cv=kfold, scoring=scoring)
		# print("Mean Squared Error: ", results.mean())
		# print("Standard Deviation: ", results.std())

		scoring = "r2"
		results = model_selection.cross_val_score(lin_model, X_train, y_train, cv=kfold, scoring=scoring)
		print("R squared val: ", results.mean())
		print("Standard Deviation: ", results.std())

		r2_score = lin_model.score(X_train,y_train)
		print("r2_score",r2_score*100,'%')

		with open('LinearRegression'+ str(userID) + '.pkl', 'wb') as pkl:
			pickle.dump(lin_model, pkl)

		return str(r2_score*100)+'%'
		
	def predict(df,hrs,userID):		
		x1,x2,x3,y=df['Usage_LastHour'],df['Usage_2Hoursback'],df['Usage_3Hoursback'],df['Usage']
		x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
		x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
		final_x=np.concatenate((x1,x2,x3),axis=1)	
		
		test = df.iloc[:hrs]		
		
		X_test,y_test=final_x[:hrs],y[:hrs]
		
		with open('LinearRegression'+ str(userID) + '.pkl', 'rb') as pkl:
			
			prediction = pickle.load(pkl).predict(X_test)
		
			print("Linear_Regression_Predictions")
			test['Linear_Regression_Predictions']=prediction

			test['Time']=test.index
			test.reset_index(drop=True, inplace=True)
			print(test[['Time','Linear_Regression_Predictions']])
			rmse_lr=sqrt(mean_squared_error(prediction,y_test))
			#print('Mean Squared Error for Linear Regression Model is:',rmse_lr)
			# r2_score = lin_model.score(X_test,y_test)
			# print("r2_score",r2_score*100,'%')
			print(test)
			return test[['Time','Linear_Regression_Predictions']]
			#return test[['Time','Linear_Regression_Predictions']],str(r2_score*100)+"%"	
	