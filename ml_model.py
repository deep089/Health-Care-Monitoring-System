import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sqlalchemy import create_engine
import joblib

class HealthRiskPredictor:
    def __init__(self, database_url='sqlite:///healthcare_db.sqlite'):
        self.engine = create_engine(database_url)
        self.model = None
        
    def prepare_data(self):
        # Load patient data from multiple tables
        query = """
        SELECT 
            p.id, p.age, p.gender, 
            m.blood_pressure, m.heart_rate, m.weight, m.height,
            l.cholesterol, l.blood_sugar, l.hemoglobin
        FROM patients p
        JOIN medical_records m ON p.id = m.patient_id
        JOIN lab_results l ON p.id = l.patient_id
        """
        
        # Read data into pandas DataFrame
        df = pd.read_sql(query, self.engine)
        
        # Preprocessing
        df['gender'] = df['gender'].map({'Male': 0, 'Female': 1})
        
        # Parse blood pressure
        df[['systolic', 'diastolic']] = df['blood_pressure'].str.split('/', expand=True).astype(float)
        df = df.drop('blood_pressure', axis=1)
        
        # Create synthetic risk label (for demonstration)
        df['high_risk'] = (
            (df['systolic'] > 140) | 
            (df['diastolic'] > 90) | 
            (df['cholesterol'] > 240) | 
            (df['blood_sugar'] > 126) | 
            (df['age'] > 60)
        ).astype(int)
        
        return df
    
    def train_model(self):
        # Prepare data
        df = self.prepare_data()
        
        # Select features
        features = ['age', 'gender', 'systolic', 'diastolic', 'heart_rate', 
                    'weight', 'height', 'cholesterol', 'blood_sugar', 'hemoglobin']
        
        X = df[features]
        y = df['high_risk']
        
        # Split and scale data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        
        # Train Random Forest Classifier
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train_scaled, y_train)
        
        # Optional: Save model and scaler
        joblib.dump(self.model, 'health_risk_model.joblib')
        joblib.dump(scaler, 'health_risk_scaler.joblib')
        
        return self.model
    
    def predict_risk(self, patient_data):
        # Load saved model and scaler if not already loaded
        if self.model is None:
            self.model = joblib.load('health_risk_model.joblib')
        
        # Scale input data
        scaler = joblib.load('health_risk_scaler.joblib')
        scaled_data = scaler.transform([patient_data])
        
        # Predict risk
        risk_probability = self.model.predict_proba(scaled_data)[0][1]
        return risk_probability

# Example usage
if __name__ == '__main__':
    predictor = HealthRiskPredictor()
    predictor.train_model()