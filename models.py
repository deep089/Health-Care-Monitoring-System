from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    
    # Relationship to medical records
    medical_records = relationship("MedicalRecord", back_populates="patient")
    lab_results = relationship("LabResult", back_populates="patient")

class MedicalRecord(Base):
    __tablename__ = 'medical_records'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    date = Column(Date, default=datetime.date.today)
    blood_pressure = Column(String)
    heart_rate = Column(Integer)
    weight = Column(Float)
    height = Column(Float)
    
    patient = relationship("Patient", back_populates="medical_records")

class LabResult(Base):
    __tablename__ = 'lab_results'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    date = Column(Date, default=datetime.date.today)
    cholesterol = Column(Float)
    blood_sugar = Column(Float)
    hemoglobin = Column(Float)
    
    patient = relationship("Patient", back_populates="lab_results")