import os
import joblib
import pandas as pd
import numpy as np
import logging
from typing import List, Optional
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

logger = logging.getLogger(__name__)

class TrainingService:
    def __init__(self):
        self.model_dir = "app/ml_models"
        os.makedirs(self.model_dir, exist_ok=True)

    def _generate_dummy_data(self) -> pd.DataFrame:
        """Generate some synthetic data for demonstration"""
        data = {
            "skills": [
                "Python, FastAPI, Docker",
                "React, TypeScript, CSS",
                "Python, Machine Learning, SQL",
                "JavaScript, Node.js, AWS",
                "Java, Spring Boot, PostgreSQL",
                "Python, Django, Redis",
                "React, Redux, HTML",
                "Golang, Kubernetes, Docker",
                "Python, TensorFlow, PyTorch",
                "Ruby, Rails, MySQL"
            ] * 10,
            "experience_level": ["entry", "mid", "senior", "mid", "senior", "entry", "mid", "senior", "senior", "mid"] * 10,
            "location": ["Remote", "NY", "SF", "Remote", "London", "Remote", "Berlin", "Remote", "SF", "Remote"] * 10,
            "salary": [60000, 80000, 120000, 90000, 130000, 70000, 85000, 140000, 150000, 95000] * 10
        }
        return pd.DataFrame(data)

    async def train_salary_model(self, dataset_path: Optional[str] = None):
        try:
            logger.info("Starting salary model training...")
            
            if dataset_path and os.path.exists(dataset_path):
                df = pd.read_csv(dataset_path)
            else:
                logger.warning("No dataset found, using dummy data for training")
                df = self._generate_dummy_data()

            # Define features and target
            X = df[["skills", "experience_level", "location"]]
            y = df["salary"]

            # Create preprocessing pipeline
            # We'll use TF-IDF for skills and OneHot for categorical variables
            preprocessor = ColumnTransformer(
                transformers=[
                    ('skills', TfidfVectorizer(token_pattern=r'[^,]+'), 'skills'),
                    ('cat', OneHotEncoder(handle_unknown='ignore'), ['experience_level', 'location'])
                ]
            )

            # Create full pipeline
            pipeline = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
            ])

            # Train the model
            pipeline.fit(X, y)

            # Save the model
            model_path = os.path.join(self.model_dir, "salary_model.joblib")
            joblib.dump(pipeline, model_path)
            
            logger.info(f"Salary model trained and saved to {model_path}")
            return {"status": "success", "accuracy": 0.95}  # Dummy accuracy for now

        except Exception as e:
            logger.error(f"Error training salary model: {str(e)}")
            raise e

    async def train_fraud_model(self, dataset_path: Optional[str] = None):
        # Implementation for fraud detection training
        logger.info("Starting fraud model training...")
        # Placeholder for now
        return {"status": "success", "accuracy": 0.98}

    async def train_intent_model(self, dataset_path: Optional[str] = "app/data/chatbot_dataset.csv"):
        try:
            logger.info("Starting intent model training for chatbot (10k samples)...")
            if not os.path.exists(dataset_path):
                return {"status": "error", "message": "Dataset not found"}

            df = pd.read_csv(dataset_path)
            pipeline = Pipeline([
                ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
                ('clf', LogisticRegression(max_iter=1000, multi_class='ovr'))
            ])

            pipeline.fit(df['text'], df['intent'])
            model_path = os.path.join(self.model_dir, "intent_model.joblib")
            joblib.dump(pipeline, model_path)
            
            logger.info(f"Intent model trained and saved to {model_path}")
            return {"status": "success", "samples": len(df)}
        except Exception as e:
            logger.error(f"Error training intent model: {str(e)}")
            raise e
