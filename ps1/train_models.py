
"""
Model Training Script for Two-Stage Fraud Detection
This script trains and saves both Stage 1 and Stage 2 models
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import logging
import os
import sys

# Add current directory to path
sys.path.append('.')

from preprocessing import DataPreprocessor
from prediction import TwoStagePredictor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_models(data_path: str, model_dir: str = "models"):
    """
    Train both Stage 1 and Stage 2 models

    Args:
        data_path: Path to training data CSV
        model_dir: Directory to save models
    """

    # Load data
    logger.info(f"Loading data from {data_path}")
    df = pd.read_csv(data_path)

    # Prepare features and target
    X = df.drop(columns=['TARGET', 'UNIQUE_ID']).copy()
    y = df['TARGET']

    logger.info(f"Data shape: {X.shape}, Target distribution: {y.value_counts().to_dict()}")

    # Initialize components
    preprocessor = DataPreprocessor()
    predictor = TwoStagePredictor()

    # ================== STAGE 1 TRAINING ==================
    logger.info("Starting Stage 1 training...")

    # Fit Stage 1 preprocessor
    preprocessor.fit_stage1(X, y)

    # Preprocess data for Stage 1
    X_stage1 = preprocessor.preprocess_stage1(X)

    # Split data for Stage 1
    X_train_s1, X_test_s1, y_train_s1, y_test_s1 = train_test_split(
        X_stage1, y, stratify=y, test_size=0.3, random_state=42
    )

    # Train Stage 1 model
    predictor.train_stage1(X_train_s1, y_train_s1)

    # Get Stage 1 predictions on test set
    stage1_probs = predictor.stage1_model.predict_proba(X_test_s1)[:, 1]
    stage1_preds = (stage1_probs > predictor.stage1_threshold).astype(int)

    # Filter data for Stage 2 (only records predicted as fraud by Stage 1)
    stage2_indices = np.where(stage1_preds == 1)[0]

    if len(stage2_indices) == 0:
        logger.error("No records predicted as fraud by Stage 1. Cannot train Stage 2.")
        return

    logger.info(f"Stage 1 sent {len(stage2_indices)} records to Stage 2")

    # ================== STAGE 2 TRAINING ==================
    logger.info("Starting Stage 2 training...")

    # Get original records that were predicted as fraud by Stage 1
    original_indices = y_test_s1.index[stage2_indices]
    stage2_df = df.loc[original_indices].copy()

    # Prepare Stage 2 data
    X_stage2_orig = stage2_df.drop(columns=['TARGET', 'UNIQUE_ID']).copy()
    y_stage2 = stage2_df['TARGET']

    logger.info(f"Stage 2 data shape: {X_stage2_orig.shape}, Target distribution: {y_stage2.value_counts().to_dict()}")

    # Fit Stage 2 preprocessor
    preprocessor.fit_stage2(X_stage2_orig, y_stage2)

    # Preprocess Stage 2 data
    X_stage2 = preprocessor.preprocess_stage2(X_stage2_orig)

    # Split Stage 2 data
    X_train_s2, X_test_s2, y_train_s2, y_test_s2 = train_test_split(
        X_stage2, y_stage2, stratify=y_stage2, test_size=0.3, random_state=42
    )

    # Train Stage 2 models
    predictor.train_stage2(X_train_s2, y_train_s2)

    # ================== SAVE MODELS ==================
    logger.info("Saving models...")

    # Create model directory
    os.makedirs(model_dir, exist_ok=True)

    # Save preprocessors
    preprocessor.save_preprocessors(model_dir)

    # Save predictors
    predictor.save_models(model_dir)

    logger.info(f"All models saved to {model_dir}")

    # ================== EVALUATION ==================
    logger.info("Evaluating models...")

    # Stage 1 evaluation
    from sklearn.metrics import classification_report, confusion_matrix

    print("\n" + "="*50)
    print("STAGE 1 EVALUATION")
    print("="*50)
    print(f"Threshold: {predictor.stage1_threshold}")
    print("\nClassification Report:")
    print(classification_report(y_test_s1, stage1_preds))

    tn, fp, fn, tp = confusion_matrix(y_test_s1, stage1_preds).ravel()
    print(f"\nConfusion Matrix: TN={tn}, FP={fp}, FN={fn}, TP={tp}")

    # Stage 2 evaluation
    if len(X_test_s2) > 0:
        # Get Stage 2 predictions
        base_predictions = []
        for name in predictor.stage2_model_names:
            if name in predictor.stage2_models:
                model = predictor.stage2_models[name]
                probs = model.predict_proba(X_test_s2)[:, 1]
                base_predictions.append(probs)

        meta_features = np.column_stack(base_predictions)
        stage2_probs = predictor.meta_model.predict_proba(meta_features)[:, 1]
        stage2_preds = (stage2_probs > predictor.stage2_threshold).astype(int)

        print("\n" + "="*50)
        print("STAGE 2 EVALUATION")
        print("="*50)
        print(f"Threshold: {predictor.stage2_threshold}")
        print("\nClassification Report:")
        print(classification_report(y_test_s2, stage2_preds))

        tn, fp, fn, tp = confusion_matrix(y_test_s2, stage2_preds).ravel()
        print(f"\nConfusion Matrix: TN={tn}, FP={fp}, FN={fn}, TP={tp}")

    logger.info("Training completed successfully!")

if __name__ == "__main__":
    # Example usage
    train_models("HACKATHON_TRAINING_DATA.csv")

    print("Model training script created.")
    print("To use this script:")
    print("1. Place your training data CSV file in the same directory")
    print("2. Run: python train_models.py")
    print("3. Models will be saved to the 'models' directory")
