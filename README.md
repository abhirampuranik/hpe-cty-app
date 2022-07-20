# hpe-cty-app

# Predicting cloud storage consumption using time-series analysis

Application uses time-series based data for prediction of future trend of storage consumption

Forecast trends for the specified time interval in the future on the trained model

Storage consumption prediction in real-time : Model trains in real time while giving future prediction 

### Client Libraries
- ReactJS
- Axios
- React-google-charts
- Material UI

### Backend(Python) Libraries
- Flask_Cors==3.0.10
- flask_restful==0.3.9
- matplotlib==3.5.1
- numpy==1.21.2
- pandas==1.3.2
- pmdarima==1.8.5
- scikit_learn==1.1.1
- tensorflow==2.9.1
- xgboost==1.6.1


### Steps to run
#### Client
``` 
cd client
npm install
npm start
```

### Flask backend
``` 
Create new environment(preferable, For conda: conda create --name myenv, conda activate myenv)
pip install -r requirements.txt
flask run
```