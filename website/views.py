from flask import Blueprint, render_template, request, send_from_directory, jsonify
import joblib
import numpy as np
import csv

views = Blueprint('views', __name__)

model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('scaler.pkl')

@views.route('/')
def home():
  csv_data = parse_csv('data_prevgrade.csv')
  return render_template("home.html", csv_data=csv_data)

@views.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = np.array(data['features']).reshape(1, -1)
    features = scaler.transform(features)
    prediction = model.predict(features)
    return jsonify({'prediction': prediction.tolist()})


def parse_csv(filepath):
   with open(filepath, mode='r', encoding='utf-8-sig') as csv_file:
      reader = csv.reader(csv_file)
      csv_data = [row for row in reader]
      return csv_data