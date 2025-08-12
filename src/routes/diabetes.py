from flask import Blueprint, request, jsonify
from src.models.diabetes import DiabetesPrediction
from src.models.user import db
from src.ml_service import ml_service

diabetes_bp = Blueprint('diabetes', __name__)

@diabetes_bp.route('/predict', methods=['POST'])
def predict_diabetes():
    data = request.get_json()
    required_fields = ['gender', 'age', 'hypertension', 'heart_disease', 'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    try:
        prediction, probability = ml_service.predict(data)
        new_prediction = DiabetesPrediction(
            gender=data['gender'],
            age=float(data['age']),
            hypertension=int(data['hypertension']),
            heart_disease=int(data['heart_disease']),
            smoking_history=data['smoking_history'],
            bmi=float(data['bmi']),
            HbA1c_level=float(data['HbA1c_level']),
            blood_glucose_level=int(data['blood_glucose_level']),
            prediction=int(prediction),
            prediction_probability=float(probability)
        )
        db.session.add(new_prediction)
        db.session.commit()
        return jsonify({'prediction': int(prediction), 'probability': float(probability)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@diabetes_bp.route('/stats', methods=['GET'])
def get_stats():
    total_predictions = DiabetesPrediction.query.count()
    positive_predictions = DiabetesPrediction.query.filter_by(prediction=1).count()
    negative_predictions = DiabetesPrediction.query.filter_by(prediction=0).count()
    
    return jsonify({
        'total_predictions': total_predictions,
        'positive_predictions': positive_predictions,
        'negative_predictions': negative_predictions
    }), 200

@diabetes_bp.route('/feature-importance', methods=['GET'])
def get_feature_importance():
    importance = ml_service.get_feature_importance()
    return jsonify(importance), 200

@diabetes_bp.route('/accuracy', methods=['GET'])
def get_model_accuracy():
    accuracy = ml_service.get_model_accuracy()
    return jsonify({'accuracy': float(accuracy) if accuracy is not None else 0.0}), 200