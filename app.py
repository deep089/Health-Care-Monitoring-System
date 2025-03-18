from flask import Flask, render_template, request, jsonify
from sqlalchemy.orm import Session
from database import get_db, init_db
from models import Patient, MedicalRecord, LabResult
from ml_model import HealthRiskPredictor
import generate_data

app = Flask(__name__)

# Predictor for risk assessment
risk_predictor = HealthRiskPredictor()

@app.route('/')
def index():
    # Get database session
    db = next(get_db())
    
    # Fetch patients
    patients = db.query(Patient).all()
    
    return render_template('index.html', patients=patients)

@app.route('/patient/<int:patient_id>')
def patient_details(patient_id):
    # Get database session
    db = next(get_db())
    
    # Fetch patient details
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    medical_records = patient.medical_records
    lab_results = patient.lab_results
    
    # Predict risk
    if medical_records and lab_results:
        latest_record = medical_records[-1]
        latest_lab = lab_results[-1]
        
        patient_data = [
            patient.age, 
            1 if patient.gender == 'Female' else 0,
            *map(float, latest_record.blood_pressure.split('/')),
            latest_record.heart_rate,
            latest_record.weight,
            latest_record.height,
            latest_lab.cholesterol,
            latest_lab.blood_sugar,
            latest_lab.hemoglobin
        ]
        
        risk_score = risk_predictor.predict_risk(patient_data)
    else:
        risk_score = None
    
    return render_template('patient_details.html', 
                           patient=patient, 
                           medical_records=medical_records,
                           lab_results=lab_results,
                           risk_score=risk_score)

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Generate sample data
    generate_data.generate_patients()
    
    # Train risk prediction model
    risk_predictor.train_model()
    
    # Run the application
    app.run(debug=True)