
"""
Data Preprocessing Module for Two-Stage Fraud Detection
Handles missing values, categorical encoding, and feature scaling
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import joblib
import logging
from typing import Dict, List, Any
import os

logger = logging.getLogger(__name__)

class DataPreprocessor:
    """Handles all data preprocessing steps"""

    def __init__(self):
        self.stage1_scaler = None
        self.stage2_scaler = None
        self.label_encoders = {}
        self.stage1_imputer = None
        self.stage2_imputer = None
        self.expected_columns = None

    def fit_stage1(self, X: pd.DataFrame, y: pd.Series = None):
        """
        Fit preprocessing components for Stage 1
        """
        logger.info("Fitting Stage 1 preprocessors...")

        # Store expected columns
        self.expected_columns = X.columns.tolist()

        # Handle missing values and encode categoricals
        X_processed = self._handle_missing_and_encode(X, fit=True)

        # Impute missing values
        self.stage1_imputer = SimpleImputer(strategy='median')
        X_imputed = pd.DataFrame(
            self.stage1_imputer.fit_transform(X_processed), 
            columns=X_processed.columns
        )

        # Scale features
        self.stage1_scaler = StandardScaler()
        self.stage1_scaler.fit(X_imputed)

        logger.info("Stage 1 preprocessors fitted successfully")

    def fit_stage2(self, X: pd.DataFrame, y: pd.Series = None):
        """
        Fit preprocessing components for Stage 2
        """
        logger.info("Fitting Stage 2 preprocessors...")

        # Handle missing values and encode categoricals
        X_processed = self._handle_missing_and_encode(X, fit=False)  # Use existing encoders

        # Impute missing values
        self.stage2_imputer = SimpleImputer(strategy='median')
        X_imputed = pd.DataFrame(
            self.stage2_imputer.fit_transform(X_processed), 
            columns=X_processed.columns
        )

        # Scale features
        self.stage2_scaler = StandardScaler()
        self.stage2_scaler.fit(X_imputed)

        logger.info("Stage 2 preprocessors fitted successfully")

    def preprocess_stage1(self, X: pd.DataFrame) -> np.ndarray:
        """
        Preprocess data for Stage 1 model
        """
        # Ensure we have all expected columns
        X = self._ensure_columns(X)

        # Handle missing values and encode categoricals
        X_processed = self._handle_missing_and_encode(X, fit=False)

        # Impute missing values
        X_imputed = pd.DataFrame(
            self.stage1_imputer.transform(X_processed), 
            columns=X_processed.columns
        )

        # Scale features
        X_scaled = self.stage1_scaler.transform(X_imputed)

        return X_scaled

    def preprocess_stage2(self, X: pd.DataFrame) -> np.ndarray:
        """
        Preprocess data for Stage 2 models
        """
        # Ensure we have all expected columns
        X = self._ensure_columns(X)

        # Handle missing values and encode categoricals
        X_processed = self._handle_missing_and_encode(X, fit=False)

        # Impute missing values
        X_imputed = pd.DataFrame(
            self.stage2_imputer.transform(X_processed), 
            columns=X_processed.columns
        )

        # Scale features
        X_scaled = self.stage2_scaler.transform(X_imputed)

        return X_scaled

    def preprocess(self, X: pd.DataFrame, stage: str = "stage1") -> np.ndarray:
        """
        General preprocessing method
        """
        if stage == "stage1":
            return self.preprocess_stage1(X)
        elif stage == "stage2":
            return self.preprocess_stage2(X)
        else:
            raise ValueError("Stage must be either 'stage1' or 'stage2'")

    def _handle_missing_and_encode(self, X: pd.DataFrame, fit: bool = False) -> pd.DataFrame:
        """
        Handle missing values and encode categorical variables
        """
        X = X.copy()

        # Replace placeholders with NaN
        X.replace(["\\N", "NA", "NaN", "null", ""], np.nan, inplace=True)

        # Encode categorical variables
        categorical_cols = X.select_dtypes(include=['object', 'category']).columns

        for col in categorical_cols:
            X[col] = X[col].astype(str)

            if fit:
                # Fit new encoder
                self.label_encoders[col] = LabelEncoder()
                X[col] = self.label_encoders[col].fit_transform(X[col])
            else:
                # Use existing encoder
                if col in self.label_encoders:
                    # Handle unseen categories
                    unique_vals = X[col].unique()
                    known_vals = self.label_encoders[col].classes_

                    # Replace unseen values with the most common known value
                    if len(known_vals) > 0:
                        most_common = known_vals[0]  # Use first class as default
                        X[col] = X[col].apply(lambda x: x if x in known_vals else most_common)

                    X[col] = self.label_encoders[col].transform(X[col])
                else:
                    # If encoder doesn't exist, use integer encoding
                    X[col] = pd.Categorical(X[col]).codes

        return X

    def _ensure_columns(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Ensure input DataFrame has all expected columns
        """
        if self.expected_columns is None:
            return X

        X = X.copy()

        # Add missing columns with NaN
        for col in self.expected_columns:
            if col not in X.columns:
                X[col] = np.nan

        # Reorder columns to match expected order
        X = X[self.expected_columns]

        return X

    def save_preprocessors(self, model_dir: str = "models"):
        """
        Save all preprocessing components
        """
        os.makedirs(model_dir, exist_ok=True)

        # Save scalers
        if self.stage1_scaler:
            joblib.dump(self.stage1_scaler, os.path.join(model_dir, "stage1_scaler.pkl"))
        if self.stage2_scaler:
            joblib.dump(self.stage2_scaler, os.path.join(model_dir, "stage2_scaler.pkl"))

        # Save imputers
        if self.stage1_imputer:
            joblib.dump(self.stage1_imputer, os.path.join(model_dir, "stage1_imputer.pkl"))
        if self.stage2_imputer:
            joblib.dump(self.stage2_imputer, os.path.join(model_dir, "stage2_imputer.pkl"))

        # Save label encoders
        if self.label_encoders:
            joblib.dump(self.label_encoders, os.path.join(model_dir, "label_encoders.pkl"))

        # Save expected columns
        if self.expected_columns:
            joblib.dump(self.expected_columns, os.path.join(model_dir, "expected_columns.pkl"))

        logger.info(f"Preprocessors saved to {model_dir}")

    def load_preprocessors(self, model_dir: str = "models"):
        """
        Load all preprocessing components
        """
        try:
            # Load scalers
            stage1_scaler_path = os.path.join(model_dir, "stage1_scaler.pkl")
            if os.path.exists(stage1_scaler_path):
                self.stage1_scaler = joblib.load(stage1_scaler_path)

            stage2_scaler_path = os.path.join(model_dir, "stage2_scaler.pkl")
            if os.path.exists(stage2_scaler_path):
                self.stage2_scaler = joblib.load(stage2_scaler_path)

            # Load imputers
            stage1_imputer_path = os.path.join(model_dir, "stage1_imputer.pkl")
            if os.path.exists(stage1_imputer_path):
                self.stage1_imputer = joblib.load(stage1_imputer_path)

            stage2_imputer_path = os.path.join(model_dir, "stage2_imputer.pkl")
            if os.path.exists(stage2_imputer_path):
                self.stage2_imputer = joblib.load(stage2_imputer_path)

            # Load label encoders
            encoders_path = os.path.join(model_dir, "label_encoders.pkl")
            if os.path.exists(encoders_path):
                self.label_encoders = joblib.load(encoders_path)

            # Load expected columns
            columns_path = os.path.join(model_dir, "expected_columns.pkl")
            if os.path.exists(columns_path):
                self.expected_columns = joblib.load(columns_path)

            logger.info(f"Preprocessors loaded from {model_dir}")

        except Exception as e:
            logger.error(f"Error loading preprocessors: {e}")
            raise

    def is_loaded(self) -> bool:
        """
        Check if preprocessors are loaded
        """
        return (self.stage1_scaler is not None and 
                self.stage1_imputer is not None)
