from src.models.user import db
from flask_sqlalchemy import SQLAlchemy

class DiabetesPrediction(db.Model):
    __tablename__ = 'diabetes_predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Float, nullable=False)
    hypertension = db.Column(db.Integer, nullable=False)
    heart_disease = db.Column(db.Integer, nullable=False)
    smoking_history = db.Column(db.String(20), nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    HbA1c_level = db.Column(db.Float, nullable=False)
    blood_glucose_level = db.Column(db.Integer, nullable=False)
    prediction = db.Column(db.Integer, nullable=False)
    prediction_probability = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def to_dict(self):
        return {
            'id': self.id,
            'gender': self.gender,
            'age': self.age,
            'hypertension': self.hypertension,
            'heart_disease': self.heart_disease,
            'smoking_history': self.smoking_history,
            'bmi': self.bmi,
            'HbA1c_level': self.HbA1c_level,
            'blood_glucose_level': self.blood_glucose_level,
            'prediction': self.prediction,
            'prediction_probability': self.prediction_probability,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }