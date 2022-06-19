import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pickle

class linearRegressionClass:
	def __init__():
		pass 

	def preprocess(df,UserID):
		#df = df.loc[:, ~df.columns.str.contains('^Unnamed')]   
		# df=pd.DataFrame()
		# df = pd.read_csv(dataset,index_col='Time',parse_dates=True)
		#df = dataset 
		df.index = df['Time']
		#df.index.freq = 'MS'
		#df.tail()
		# df.columns = ['Usage']
		#df.plot(figsize=(12,8))

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
        
        #print("reached")
		print(df.head())

		# x1,x2,x3,y=df['Usage_LastHour'],df['Usage_2Hoursback'],df['Usage_3Hoursback'],df['Usage']
		# x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
		# x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
		# final_x=np.concatenate((x1,x2,x3),axis=1)

		return df

	def train(df):  	
		lin_model=LinearRegression()		
		x1,x2,x3,y=df['Usage_LastHour'],df['Usage_2Hoursback'],df['Usage_3Hoursback'],df['Usage']
		x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
		x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
		final_x=np.concatenate((x1,x2,x3),axis=1)		

		# test_ind = len(df) - 30
		# train = df.iloc[:test_ind]
		# test = df.iloc[test_ind:]
		# X_train,X_test,y_train,y_test=final_x[:-30],final_x[-30:],y[:-30],y[-30:]
		X_train,X_test,y_train,y_test=final_x,final_x,y,y
		#X_train,X_test,y_train,y_test=df[:-30],df[-30:],df[:-30],df[-30:]

		lin_model.fit(X_train,y_train) 
		with open('LinearRegression.pkl', 'wb') as pkl:
			pickle.dump(lin_model, pkl)
		#return X_test 

	# def predict(test):
	# 	test_size = len(test)
	# 	with open('LinearRegression.pkl', 'rb') as pkl:
	# 		#prediction = pd.DataFrame(pickle.load(pkl).predict(n_periods=test_size),index=test.index)
	# 		prediction = pd.DataFrame(pickle.load(pkl).predict(test_size),index=test.index)
	# 		prediction.columns = ['Usage']
	# 		print(prediction)
	# 		return prediction

	def predict(df):
		#test_size = len(test)
		x1,x2,x3,y=df['Usage_LastHour'],df['Usage_2Hoursback'],df['Usage_3Hoursback'],df['Usage']
		x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
		x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
		final_x=np.concatenate((x1,x2,x3),axis=1)	

		X_train,X_test,y_train,y_test=final_x,final_x,y,y	

		with open('LinearRegression.pkl', 'rb') as pkl:
			#prediction = pd.DataFrame(pickle.load(pkl).predict(n_periods=test_size),index=test.index)
			prediction = pd.DataFrame(pickle.load(pkl).predict(X_test))
			#lin_pred=lin_model.predict(X_test)
    		#print("Linear_Regression_Predictions")
    		#test['Linear_Regression_Predictions']=lin_pred
			prediction.columns = ['Pred']
			#prediction.columns = ['Usage']
			print()
			return prediction

	def update(df):
		lin_model=LinearRegression()
		x1,x2,x3,y=df['Usage_LastHour'],df['Usage_2Hoursback'],df['Usage_3Hoursback'],df['Usage']
		x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
		x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
		final_x=np.concatenate((x1,x2,x3),axis=1)	

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


# Linear Regression

@app.route('/linearRegression/train',methods=['POST'])
def linearRegression_train():
    file = request.files['file']
    userID = int(request.form['userID'])
    df = pd.read_csv(file)
    print("initial")
    print(df)
    #df = linearRegressionClass.preprocess(df[df['UserID'] == userID] )
    df = linearRegressionClass.preprocess(df,userID)
    print("after preprocess")
    print(df)
    linearRegressionClass.train(df)
    return "Model Trained Successfully"   

@app.route('/linearRegression/update',methods=['POST'])
def linearRegression_update():
    file = request.files['file']
    userID = int(request.form['userID'])
    df = pd.read_csv('LR_Predict.csv')
    print("initial mmm")
    print(df)
    #df=pd.read_csv('LR_Predict.csv')
    #df = linearRegressionClass.preprocess(df[df['UserID'] == userID])
    df = linearRegressionClass.preprocess(df,userID)
    print("after")
    print(df)
    linearRegressionClass.update(df)
    return "Updated Model Successfully"  

@app.route('/linearRegression/predict',methods=['POST'])
def linearRegression_predict():
    days = request.json['body']['days']
    hours = request.json['body']['hours']
    userID = request.json['body']['userID']
    print(userID)
    print(type(userID))
    #userID = int(request.form['userID'])
    # df = pd.read_csv(file)
    dg = DateGenML()
    msg = dg.date_df(int(days)*24 + int(hours), int(userID))    
    print(msg)
    print("initial data")
    df=pd.read_csv('LR_Predict.csv')
    print(df)
    df = linearRegressionClass.preprocess(df,int(userID))
    print("after preprocess")
    print(df)
    # df = AutoArima.preprocess(df,1)
    preds = linearRegressionClass.predict(df)
    # print(preds)
    response=preds
    return response.to_csv() 