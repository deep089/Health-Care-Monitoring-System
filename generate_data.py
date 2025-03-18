import random
from faker import Faker
from database import SessionLocal, init_db
from models import Patient, MedicalRecord, LabResult
import datetime

fake = Faker()

def generate_patients(num_patients=30):
    """Generate dummy patient data"""
    db = SessionLocal()
    
    # Clear existing data
    db.query(LabResult).delete()
    db.query(MedicalRecord).delete()
    db.query(Patient).delete()
    
    patients = []
    for _ in range(num_patients):
        # Generate patient
        patient = Patient(
            name=fake.name(),
            age=random.randint(18, 85),
            gender=random.choice(['Male', 'Female'])
        )
        db.add(patient)
        patients.append(patient)
        
        # Generate medical records
        for _ in range(random.randint(1, 3)):
            medical_record = MedicalRecord(
                patient=patient,
                date=fake.date_between(start_date='-2y', end_date='today'),
                blood_pressure=f"{random.randint(100, 180)}/{random.randint(60, 120)}",
                heart_rate=random.randint(60, 100),
                weight=round(random.uniform(50, 120), 1),
                height=round(random.uniform(150, 200), 1)
            )
            db.add(medical_record)
        
        # Generate lab results
        for _ in range(random.randint(1, 3)):
            lab_result = LabResult(
                patient=patient,
                date=fake.date_between(start_date='-2y', end_date='today'),
                cholesterol=round(random.uniform(100, 300), 1),
                blood_sugar=round(random.uniform(70, 200), 1),
                hemoglobin=round(random.uniform(10, 18), 1)
            )
            db.add(lab_result)
    
    db.commit()
    db.close()
    print(f"Generated data for {num_patients} patients")

if __name__ == '__main__':
    init_db()
    generate_patients()