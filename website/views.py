from flask import Blueprint, render_template, request, send_from_directory, jsonify
import joblib
import numpy as np

views = Blueprint('views', __name__)

model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('scaler.pkl')

@views.route('/')
def home():
  return render_template("home.html")

@views.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = np.array(data['features']).reshape(1, -1)
    features = scaler.transform(features)
    prediction = model.predict(features)
    return jsonify({'prediction': prediction.tolist()})