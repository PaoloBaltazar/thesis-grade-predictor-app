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
@views.route('/')
def home(): 
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    # Fetch previous data from the database for the current user only
    input_prediction_data = Data.query.filter_by(user_id=current_user.id).all()

    # Prepare data for the first accordion (Inputs and Predicted Grades)
    csv_data = [
        {
            'attendance': row.attendance,
            'previous_grades': row.previousGrade,
            'financial_situation': row.financialSituation,
            'learning_environment': row.learningEnvironment,
            'grade_level': row.gradeLevel,
            'predicted_grade': row.predictedGrade
        }
        for row in input_prediction_data
    ]

    # Prepare data for the second accordion (Student No. and Predicted Grade)
    stored_predictions = [
        {'student_id': row.id, 'predicted_grade': row.predictedGrade}
        for row in input_prediction_data
    ]

    return render_template("home.html", csv_data=csv_data, stored_predictions=stored_predictions)


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

    # Predict the grade
    features = np.array([attendance, financial_situation, learning_environment, previous_grades, grade_level]).reshape(1, -1)
    features = scaler.transform(features)
    prediction = model.predict(features)[0]

    # Create a new data entry in the database
    new_data = Data(
        attendance=attendance,
        previousGrade=previous_grades,
        financialSituation=financial_situation,
        learningEnvironment=learning_environment,
        gradeLevel=grade_level,
        predictedGrade=prediction,
        user_id=current_user.id  # Store the current user's ID
    )
    
    db.session.add(new_data)
    db.session.commit()

    # Return the prediction and the auto-incremented ID as a JSON response
    return jsonify({
        'prediction': prediction,
        'student_id': new_data.id  # Returning the new ID (auto-incremented)
    })


def parse_csv(filepath):
   with open(filepath, mode='r', encoding='utf-8-sig') as csv_prevdata:
      reader = csv.reader(csv_prevdata)
      csv_prevdata = [row for row in reader]
      return csv_prevdata
   
@views.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('views.home'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('views.home'))

    if file and file.filename.endswith('.csv'):
        # Ensure the upload directory exists
        if not os.path.exists(UPLOAD_FOLDER):
            try:
                os.makedirs(UPLOAD_FOLDER)  # Create the directory
            except OSError as e:
                return f"Error creating upload directory: {e}"

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)

        try:
            # Save the uploaded file
            file.save(filepath)
        except PermissionError as e:
            return f"Permission error: {e}"

        # Process the CSV file (rest of your logic)
        df = pd.read_csv(filepath)
        # Further code to process and make predictions

        return redirect(url_for('views.home'))

    return redirect(url_for('views.home'))