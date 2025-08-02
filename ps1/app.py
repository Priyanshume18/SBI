
"""
FastAPI Application for Two-Stage Fraud Detection Model
Stage 1: XGBoost classifier with threshold 0.3
Stage 2: Ensemble of 7 models + Logistic Regression meta-model with threshold 0.05
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import logging
from typing import Dict, Any, List, Optional
import os
from datetime import datetime

from preprocessing import DataPreprocessor
from prediction import TwoStagePredictor

from fastapi.middleware.cors import CORSMiddleware



# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Two-Stage Fraud Detection API",
    description="API for fraud detection using a two-stage machine learning pipeline",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize components
preprocessor = DataPreprocessor()
predictor = TwoStagePredictor()

class PredictionRequest(BaseModel):
    """Request model for prediction endpoint"""
    data: Dict[str, Any]

    class Config:
        schema_extra = {
            "example": {
                "data": {
                    "ACCT_AGE": 1.613,
                    "LIMIT": 1005500.0,
                    "OUTS": 494161.89,
                    "ACCT_RESIDUAL_TENURE": 0.890,
                    "LOAN_TENURE": 914,
                    "INSTALAMT": 38513.0,
                    "SI_FLG": "Y",
                    "AGE": 57.663,
                    "VINTAGE": 18.601,
                    "KYC_SCR": 110.0
                    # ... include other required features
                }
            }
        }

class PredictionResponse(BaseModel):
    """Response model for prediction endpoint"""
    prediction: int
    stage1_probability: float
    stage2_probability: Optional[float] = None 
    stage_used: str
    processing_time_ms: float
    timestamp: str

@app.on_event("startup")
async def startup_event():
    """Load models on startup"""
    try:
        predictor.load_models()
        preprocessor.load_preprocessors()
        logger.info("Models loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load models: {e}")
        raise

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Two-Stage Fraud Detection API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "stage1_model_loaded": predictor.stage1_model is not None,
        "stage2_models_loaded": len(predictor.stage2_models) > 0,
        "meta_model_loaded": predictor.meta_model is not None,
        "preprocessors_loaded": preprocessor.is_loaded(),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Make fraud prediction using two-stage model

    Returns:
    - prediction: 0 (not fraud) or 1 (fraud)
    - stage1_probability: probability from stage 1 model
    - stage2_probability: probability from stage 2 model (if used)
    - stage_used: "stage1" or "stage2"
    - processing_time_ms: time taken for prediction
    """
    start_time = datetime.now()

    try:
        # Convert request data to DataFrame
        df = pd.DataFrame([request.data])

        # Preprocess the data
        processed_data = preprocessor.preprocess(df)

        # Make prediction using two-stage model
        result = predictor.predict(processed_data)

        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000

        return PredictionResponse(
            prediction=result["prediction"],
            stage1_probability=result["stage1_probability"],
            stage2_probability=result.get("stage2_probability"),
            stage_used=result["stage_used"],
            processing_time_ms=round(processing_time, 2),
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/predict_batch")
async def predict_batch(requests: List[PredictionRequest]):
    """
    Make batch predictions for multiple records
    """
    start_time = datetime.now()

    try:
        results = []

        for req in requests:
            # Convert request data to DataFrame
            df = pd.DataFrame([req.data])

            # Preprocess the data
            processed_data = preprocessor.preprocess(df)

            # Make prediction
            result = predictor.predict(processed_data)
            results.append(result)

        processing_time = (datetime.now() - start_time).total_seconds() * 1000

        return {
            "predictions": results,
            "total_processing_time_ms": round(processing_time, 2),
            "records_processed": len(requests),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")

@app.get("/model_info")
async def get_model_info():
    """Get information about loaded models"""
    try:
        return predictor.get_model_info()
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get model info: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
