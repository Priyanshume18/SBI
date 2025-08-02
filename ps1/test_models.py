"""
Test script to verify all 7 Stage 2 models are loading correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prediction import TwoStagePredictor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_model_loading():
    """Test if all models load correctly"""
    print("Testing model loading...")
    
    predictor = TwoStagePredictor()
    
    try:
        # Load models
        predictor.load_models()
        
        # Get model info
        info = predictor.get_model_info()
        
        print("\n=== Model Loading Results ===")
        print(f"Stage 1 model loaded: {info['stage1_model_loaded']}")
        print(f"Stage 2 models loaded: {info['stage2_models_loaded']}")
        print(f"Stage 2 models missing: {info['stage2_models_missing']}")
        print(f"Stage 2 models count: {info['stage2_models_count']}/{info['stage2_expected_count']}")
        print(f"Meta model loaded: {info['meta_model_loaded']}")
        print(f"All Stage 2 models loaded: {info['all_stage2_models_loaded']}")
        
        if not info['all_stage2_models_loaded']:
            print(f"\n⚠️  WARNING: Missing models: {info['stage2_models_missing']}")
            print("This will cause the 500 error because the meta-model expects 7 features!")
        else:
            print("\n✅ SUCCESS: All 7 Stage 2 models loaded correctly!")
            
    except Exception as e:
        print(f"\n❌ ERROR loading models: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_model_loading()
