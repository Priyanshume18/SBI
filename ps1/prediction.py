
"""
Two-Stage Prediction Module
Stage 1: XGBoost with threshold 0.3
Stage 2: Ensemble of 7 models + LogisticRegression meta-model with threshold 0.05
"""

import pandas as pd
import numpy as np
import joblib
import logging
from typing import Dict, List, Any
import os
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
import xgboost as xgb
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

logger = logging.getLogger(__name__)

class TwoStagePredictor:
    """Two-stage fraud detection predictor"""

    def __init__(self):
        # Stage 1
        self.stage1_model = None
        self.stage1_threshold = 0.3

        # Stage 2
        self.stage2_models = {}
        self.meta_model = None
        self.stage2_threshold = 0.05

        # Model names for Stage 2
        self.stage2_model_names = [
            'XGBoost', 'LightGBM', 'CatBoost', 'ExtraTrees', 
            'MLP', 'LogisticRegression', 'RandomForest'
        ]

    def create_stage1_model(self, scale_pos_weight: float = None):
        """
        Create Stage 1 XGBoost model
        """
        self.stage1_model = xgb.XGBClassifier(
            use_label_encoder=False,
            eval_metric='logloss',
            scale_pos_weight=scale_pos_weight,
            max_depth=6,
            learning_rate=0.1,
            n_estimators=100,
            objective='binary:logistic',
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        )
        return self.stage1_model

    def create_stage2_models(self):
        """
        Create Stage 2 ensemble models
        """
        self.stage2_models = {
            'XGBoost': xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42),
            'LightGBM': LGBMClassifier(random_state=42, verbose=-1),
            'CatBoost': CatBoostClassifier(verbose=0, random_state=42),
            'ExtraTrees': ExtraTreesClassifier(random_state=42),
            'MLP': MLPClassifier(max_iter=300, random_state=42),
            'LogisticRegression': LogisticRegression(max_iter=500, random_state=42),
            'RandomForest': RandomForestClassifier(random_state=42)
        }

        # Meta-model
        self.meta_model = LogisticRegression(max_iter=1000, random_state=42)

        return self.stage2_models, self.meta_model

    def train_stage1(self, X_train: np.ndarray, y_train: np.ndarray):
        """
        Train Stage 1 model
        """
        logger.info("Training Stage 1 model...")

        # Calculate scale_pos_weight
        neg, pos = np.bincount(y_train)
        scale_pos_weight = neg / pos if pos > 0 else 1.0

        # Create and train model
        if self.stage1_model is None:
            self.create_stage1_model(scale_pos_weight)

        self.stage1_model.fit(X_train, y_train)
        logger.info("Stage 1 model trained successfully")

    def train_stage2(self, X_train: np.ndarray, y_train: np.ndarray):
        """
        Train Stage 2 ensemble models and meta-model
        """
        logger.info("Training Stage 2 models...")

        # Create models if they don't exist
        if not self.stage2_models:
            self.create_stage2_models()

        # Train base models and collect predictions
        base_predictions = []

        for name, model in self.stage2_models.items():
            logger.info(f"Training {name}...")
            model.fit(X_train, y_train)
            probs = model.predict_proba(X_train)[:, 1]
            base_predictions.append(probs)

        # Prepare meta-features (predictions from base models)
        meta_features = np.column_stack(base_predictions)

        # Train meta-model
        logger.info("Training meta-model...")
        self.meta_model.fit(meta_features, y_train)

        logger.info("Stage 2 models trained successfully")

    def predict(self, X: np.ndarray) -> Dict[str, Any]:
        """
        Make prediction using two-stage approach

        Args:
            X: Preprocessed input features

        Returns:
            Dictionary containing prediction results
        """
        if self.stage1_model is None:
            raise ValueError("Stage 1 model not loaded")

        # Stage 1 prediction
        stage1_probs = self.stage1_model.predict_proba(X)[:, 1]
        stage1_pred = (stage1_probs > self.stage1_threshold).astype(int)

        result = {
            "stage1_probability": float(stage1_probs[0]),
            "stage1_prediction": int(stage1_pred[0])
        }

        # If Stage 1 predicts 0 (not fraud), return immediately
        if stage1_pred[0] == 0:
            result.update({
                "prediction": 0,
                "stage_used": "stage1",
                "stage2_probability": None
            })
            return result

        # If Stage 1 predicts 1 (fraud), proceed to Stage 2
        if not self.stage2_models or self.meta_model is None:
            raise ValueError("Stage 2 models not loaded")

        # Get predictions from all Stage 2 base models
        base_predictions = []
        loaded_models = []
        for name in self.stage2_model_names:
            if name in self.stage2_models:
                model = self.stage2_models[name]
                probs = model.predict_proba(X)[:, 1]
                base_predictions.append(probs[0])
                loaded_models.append(name)

        logger.info(f"Stage 2 models used: {loaded_models} (total: {len(loaded_models)})")
        
        if len(base_predictions) != 7:
            logger.warning(f"Expected 7 models but only {len(base_predictions)} models loaded: {loaded_models}")

        # Meta-model prediction
        meta_features = np.array(base_predictions).reshape(1, -1)
        stage2_probs = self.meta_model.predict_proba(meta_features)[:, 1]
        stage2_pred = (stage2_probs > self.stage2_threshold).astype(int)

        result.update({
            "prediction": int(stage2_pred[0]),
            "stage_used": "stage2",
            "stage2_probability": float(stage2_probs[0])
        })

        return result

    def predict_batch(self, X: np.ndarray) -> List[Dict[str, Any]]:
        """
        Make batch predictions
        """
        results = []
        for i in range(X.shape[0]):
            result = self.predict(X[i:i+1])
            results.append(result)
        return results

    def save_models(self, model_dir: str = "models"):
        """
        Save all models
        """
        os.makedirs(model_dir, exist_ok=True)

        # Save Stage 1 model
        if self.stage1_model:
            self.stage1_model.save_model(os.path.join(model_dir, "stage1_xgboost.json"))

        # Save Stage 2 models
        for name, model in self.stage2_models.items():
            if hasattr(model, 'save_model'):
                # For XGBoost, LightGBM, CatBoost
                if name == 'XGBoost':
                    model.save_model(os.path.join(model_dir, f"stage2_{name.lower()}.json"))
                elif name == 'LightGBM':
                    model.booster_.save_model(os.path.join(model_dir, f"stage2_{name.lower()}.txt"))
                elif name == 'CatBoost':
                    model.save_model(os.path.join(model_dir, f"stage2_{name.lower()}.cbm"))
            else:
                # For sklearn models
                joblib.dump(model, os.path.join(model_dir, f"stage2_{name.lower()}.pkl"))

        # Save meta-model
        if self.meta_model:
            joblib.dump(self.meta_model, os.path.join(model_dir, "meta_model.pkl"))

        # Save thresholds
        thresholds = {
            'stage1_threshold': self.stage1_threshold,
            'stage2_threshold': self.stage2_threshold
        }
        joblib.dump(thresholds, os.path.join(model_dir, "thresholds.pkl"))

        logger.info(f"Models saved to {model_dir}")

    def load_models(self, model_dir: str = "models"):
        """
        Load all models
        """
        try:
            # Load Stage 1 model
            stage1_path = os.path.join(model_dir, "stage1_xgboost.json")
            if os.path.exists(stage1_path):
                self.stage1_model = xgb.XGBClassifier()
                self.stage1_model.load_model(stage1_path)

            # Load Stage 2 models
            self.stage2_models = {}

            # XGBoost
            xgb_path = os.path.join(model_dir, "stage2_xgboost.json")
            if os.path.exists(xgb_path):
                xgb_model = xgb.XGBClassifier()
                xgb_model.load_model(xgb_path)
                self.stage2_models['XGBoost'] = xgb_model

            # LightGBM
            lgb_pkl_path = os.path.join(model_dir, "stage2_lightgbm.pkl")
            if os.path.exists(lgb_pkl_path):
                self.stage2_models['LightGBM'] = joblib.load(lgb_pkl_path)

            # CatBoost
            cb_path = os.path.join(model_dir, "stage2_catboost.cbm")
            if os.path.exists(cb_path):
                cb_model = CatBoostClassifier()
                cb_model.load_model(cb_path)
                self.stage2_models['CatBoost'] = cb_model

            # Other sklearn models
            for name in ['ExtraTrees', 'MLP', 'LogisticRegression', 'RandomForest']:
                model_path = os.path.join(model_dir, f"stage2_{name.lower()}.pkl")
                if os.path.exists(model_path):
                    self.stage2_models[name] = joblib.load(model_path)

            # Load meta-model
            meta_path = os.path.join(model_dir, "meta_model.pkl")
            if os.path.exists(meta_path):
                self.meta_model = joblib.load(meta_path)

            # Load thresholds
            thresholds_path = os.path.join(model_dir, "thresholds.pkl")
            if os.path.exists(thresholds_path):
                thresholds = joblib.load(thresholds_path)
                self.stage1_threshold = thresholds['stage1_threshold']
                self.stage2_threshold = thresholds['stage2_threshold']

            logger.info(f"Models loaded from {model_dir}")

        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about loaded models
        """
        loaded_stage2_models = list(self.stage2_models.keys())
        missing_stage2_models = [name for name in self.stage2_model_names if name not in loaded_stage2_models]
        
        return {
            "stage1_model_loaded": self.stage1_model is not None,
            "stage1_threshold": self.stage1_threshold,
            "stage2_models_loaded": loaded_stage2_models,
            "stage2_models_missing": missing_stage2_models,
            "stage2_models_count": len(self.stage2_models),
            "stage2_expected_count": len(self.stage2_model_names),
            "meta_model_loaded": self.meta_model is not None,
            "stage2_threshold": self.stage2_threshold,
            "all_stage2_models_loaded": len(loaded_stage2_models) == len(self.stage2_model_names)
        }
