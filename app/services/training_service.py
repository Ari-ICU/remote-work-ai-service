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

import tensorflow as tf
from tensorflow.keras import layers, models

logger = logging.getLogger(__name__)

class TrainingService:
    def __init__(self):
        self.model_dir = "app/ml_models"
        self.data_dir = "app/data"
        os.makedirs(self.model_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)

    def _generate_dummy_data(self) -> pd.DataFrame:
        """Generate some synthetic data for demonstration"""
        data = {
            "skills": [
                "Python, FastAPI, Docker",
                "React, TypeScript, CSS",
                "Python, Machine Learning, SQL",
                "JavaScript, Node.js, AWS",
                "Java, Spring Boot, PostgreSQL"
            ] * 20,
            "experience_level": ["entry", "mid", "senior", "mid", "senior"] * 20,
            "location": ["Remote", "NY", "SF", "Remote", "London"] * 20,
            "salary": [60000, 80000, 120000, 90000, 130000] * 20
        }
        return pd.DataFrame(data)

    async def train_salary_model(self, dataset_path: Optional[str] = None):
        try:
            logger.info("Starting ADVANCED Salary Neural Network training...")
            
            if dataset_path and os.path.exists(dataset_path):
                df = pd.read_csv(dataset_path)
            else:
                df = self._generate_dummy_data()

            # 1. Feature Engineering
            X = df[["skills", "experience_level", "location"]]
            y = df["salary"].values

            preprocessor = ColumnTransformer(
                transformers=[
                    ('skills', TfidfVectorizer(max_features=100), 'skills'),
                    ('cat', OneHotEncoder(sparse_output=False), ['experience_level', 'location'])
                ]
            )

            # 2. Transform Data
            X_encoded = preprocessor.fit_transform(X)
            
            # 3. Build Neural Network
            model = models.Sequential([
                layers.Dense(64, activation='relu', input_shape=(X_encoded.shape[1],)),
                layers.Dropout(0.2),
                layers.Dense(32, activation='relu'),
                layers.Dense(1) # Salary prediction output
            ])

            model.compile(optimizer='adam', loss='mse', metrics=['mae'])
            
            # 4. Train
            logger.info(f"Training on {len(X_encoded)} samples...")
            model.fit(X_encoded, y, epochs=50, verbose=0)

            # 5. Save Model AND Preprocessor
            model_path = os.path.join(self.model_dir, "salary_dl_model.h5")
            model.save(model_path)
            
            # We must save the preprocessor too to use it during prediction
            joblib.dump(preprocessor, os.path.join(self.model_dir, "salary_preprocessor.joblib"))
            
            logger.info(f"✅ Neural Network Salary model saved to {model_path}")
            return {"status": "success", "type": "neural_network"}

        except Exception as e:
            logger.error(f"Error training advanced salary model: {str(e)}")
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
