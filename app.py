from flask import Flask, render_template, url_for, request
import pandas as pd
import pickle

model = pickle.load(open('pickle-files/xgboost.pkl', 'rb'))
app = Flask(__name__)

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
  df = pd.read_csv('data_2018.csv')
  predictions = model.predict(df.iloc[:,:-1].values)
  predictions = predictions.tolist()
  df2 = pd.read_csv('assets/aqi/aqi2018.csv')
  actuals = df2.iloc[:,-2]
  actuals = actuals.tolist()
  return render_template('result.html', output=zip(predictions,actuals))

if __name__ == "__main__":
  app.run(debug=True)
