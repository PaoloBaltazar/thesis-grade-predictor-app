from flask import Blueprint, render_template, request, send_from_directory, jsonify, redirect, url_for
import pandas as pd
import joblib
import numpy as np
import csv
import os

views = Blueprint('views', __name__)

model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('scaler.pkl')

UPLOAD_FOLDER = 'uploads'

@views.route('/')
def home():
    csv_prevdata = parse_csv('data_prevgrade.csv')
    csv_data = []  # Initialize as an empty list for the predicted data
    return render_template("home.html", csv_prevdata=csv_prevdata, csv_data=csv_data)

@views.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = np.array(data['features']).reshape(1, -1)
    features = scaler.transform(features)
    prediction = model.predict(features)
    return jsonify({'prediction': prediction.tolist()})


def parse_csv(filepath):
   with open(filepath, mode='r', encoding='utf-8-sig') as csv_prevdata:
      reader = csv.reader(csv_prevdata)
      csv_prevdata = [row for row in reader]
      return csv_prevdata
   
@views.route('/upload', methods=['POST'])
def upload_file():
    csv_prevdata = parse_csv('data_prevgrade.csv')  # Parse the previous grade data
    if 'file' not in request.files:
        return redirect(url_for('views.home'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('views.home'))

    if file and file.filename.endswith('.csv'):
        # Ensure the upload directory exists
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Process the CSV file
        df = pd.read_csv(filepath)
        features = df[['attendance', 'financial_situation', 'learning_environment', 'previous_grades']]
        X_scaled = scaler.transform(features)
        predictions = model.predict(X_scaled)

        # Prepare data to be rendered in the template
        predicted_df = pd.DataFrame({
            'Index': df.index,
            'Predicted Grade': predictions
        })

        # Convert the DataFrame to a dictionary to pass to the template
        csv_data = predicted_df.to_dict('records')

        return render_template("home.html", csv_prevdata=csv_prevdata, csv_data=csv_data)
    return redirect(url_for('views.home'))