import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

class MLService:
    def __init__(self):
        self.model = None
        self.feature_names = None
        self.accuracy = None
        self.model_path = os.path.join(os.path.dirname(__file__), 'diabetes_model.pkl')
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'diabetes_prediction_dataset.csv')
        self.load_or_train_model()

    def load_or_train_model(self):
        if os.path.exists(self.model_path):
            print("Loading existing model...")
            self.model, self.feature_names, self.accuracy = joblib.load(self.model_path)
        else:
            print("Training new model...")
            self.train_model()
            print("Model trained and saved successfully!")

    def train_model(self):
        try:
            df = pd.read_csv(self.data_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Dataset not found at: {self.data_path}")

        df['gender'] = df['gender'].map({'Male': 0, 'Female': 1, 'Other': 2})
        df['smoking_history'] = df['smoking_history'].map({
            'never': 0, 'No Info': 1, 'current': 2, 'ever': 3, 'former': 4, 'not current': 5
        })

        X = df.drop('diabetes', axis=1)
        y = df['diabetes']
        self.feature_names = X.columns.tolist()

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model = RandomForestClassifier(random_state=42)
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        self.accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {self.accuracy}")

        joblib.dump((self.model, self.feature_names, self.accuracy), self.model_path)

    def predict(self, data):
        input_df = pd.DataFrame([data])
        input_df['gender'] = input_df['gender'].map({'Male': 0, 'Female': 1, 'Other': 2})
        input_df['smoking_history'] = input_df['smoking_history'].map({
            'never': 0, 'No Info': 1, 'current': 2, 'ever': 3, 'former': 4, 'not current': 5
        })
        input_df = input_df[self.feature_names]
        prediction = self.model.predict(input_df)[0]
        probability = self.model.predict_proba(input_df)[0][1]
        return prediction, probability

    def get_feature_importance(self):
        if self.model and self.feature_names:
            importances = self.model.feature_importances_
            features = self.feature_names
            return dict(zip(features, importances))
        return {}

    def get_model_accuracy(self):
        return self.accuracy

ml_service = MLService()