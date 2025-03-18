# Health-Care-Monitoring-System
A comprehensive healthcare data management and monitoring application built with Flask and SQLAlchemy, designed to track patient vitals and lab results over time.

## Overview

This Healthcare Monitoring System provides a robust platform for healthcare providers to:
- Store and manage patient demographic information
- Record and monitor vital signs and medical measurements
- Track laboratory results over time
- Generate predictive insights based on patient data

## Technologies

- **Backend Framework**: Flask
- **ORM**: SQLAlchemy
- **Database**: SQL (compatible with SQLite, PostgreSQL, MySQL)
- **Data Analysis**: Integrated prediction models

## Data Models

The system is built on three core data models:

### Patient
Stores essential patient demographic information:
- ID (primary key)
- Name
- Age
- Gender

### Medical Record
Captures vital signs and physical measurements:
- ID (primary key)
- Patient ID (foreign key)
- Date
- Blood Pressure
- Heart Rate
- Weight
- Height

### Lab Result
Tracks laboratory test results:
- ID (primary key)
- Patient ID (foreign key)
- Date
- Cholesterol Level
- Blood Sugar Level
- Hemoglobin Level

## Key Features

- **Relational Data Structure**: Efficiently connects patients with their medical records and lab results
- **Longitudinal Tracking**: Monitor changes in patient health metrics over time
- **Data Validation**: Ensures integrity of medical information
- **Predictive Analytics**: Leverages historical data to predict potential health trends

## Installation

1. Clone this repository
```bash
git clone https://github.com/yourusername/healthcare-monitoring-system.git
cd healthcare-monitoring-system
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Initialize the database
```bash
python init_db.py
```

5. Start the application
```bash
python app.py
```

## Usage

### Creating a New Patient
```python
from models import Patient, MedicalRecord, LabResult
from database import Session

# Create a database session
session = Session()

# Create a new patient
new_patient = Patient(name="John Doe", age=45, gender="Male")
session.add(new_patient)
session.commit()
```

### Recording Medical Data
```python
# Add medical record for existing patient
med_record = MedicalRecord(
    patient_id=1,
    blood_pressure="120/80",
    heart_rate=72,
    weight=70.5,
    height=175.5
)
session.add(med_record)
session.commit()
```

### Retrieving Patient History
```python
# Get patient with all associated records
patient = session.query(Patient).filter_by(id=1).first()
print(f"Patient: {patient.name}")

# Access medical records
for record in patient.medical_records:
    print(f"Date: {record.date}, BP: {record.blood_pressure}, HR: {record.heart_rate}")

# Access lab results
for result in patient.lab_results:
    print(f"Date: {result.date}, Blood Sugar: {result.blood_sugar}")
```

## Predictive Analysis

The system includes prediction models that analyze historical patient data to identify potential health risks and trends. The prediction module uses patterns in vital signs and lab results to generate alerts for healthcare providers.


