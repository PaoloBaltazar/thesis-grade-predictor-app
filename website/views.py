from flask import Blueprint, render_template, request, send_from_directory, jsonify, redirect, url_for
import pandas as pd
import joblib
import numpy as np
import csv
import os
from .db_model import Data, User
from . import db
from flask_login import current_user

views = Blueprint('views', __name__)

model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('scaler.pkl')

UPLOAD_FOLDER = 'uploads'

@views.route('/')
def home(): 
    # Fetch previous grade data from CSV file
    csv_prevdata = parse_csv('data_prevgrade.csv')
    
    # Fetch user-specific data from the database
    user_data = Data.query.filter_by(user_id=current_user.id).all() if current_user.is_authenticated else []

    # Prepare data for rendering in the template
    csv_data = [
        {
            'attendance': row.attendance,
            'previous_grades': row.previousGrade,
            'financial_situation': row.financialSituation,
            'learning_environment': row.learningEnvironment,
            'grade_level': row.gradeLevel,
            'predicted_grade': row.predictedGrade
        }
        for row in user_data
    ]

    return render_template("home.html", csv_prevdata=csv_prevdata, csv_data=csv_data)

@views.route('/predict', methods=['POST'])
def predict():
    if not current_user.is_authenticated:
        return jsonify({'error': 'User not authenticated'}), 401

    data = request.json
    try:
        attendance = float(data['attendance'])
        previous_grades = float(data['previous_grades'])
        financial_situation = float(data['financial_situation'])
        learning_environment = float(data['learning_environment'])
        grade_level = int(data['grade_level'])
    except (KeyError, ValueError) as e:
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400

    features = np.array([attendance, financial_situation, learning_environment, previous_grades, grade_level]).reshape(1, -1)
    features = scaler.transform(features)
    prediction = model.predict(features)[0]

    # Save data and prediction to the database
    new_data = Data(
        attendance=attendance,
        previousGrade=previous_grades,
        financialSituation=financial_situation,
        learningEnvironment=learning_environment,
        gradeLevel=grade_level,
        predictedGrade=prediction,
        user_id=current_user.id
    )
    db.session.add(new_data)
    db.session.commit()

    return jsonify({'prediction': prediction})


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
        features = df[['attendance', 'financial_situation', 'learning_environment', 'grade_level', 'previous_grades']]
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