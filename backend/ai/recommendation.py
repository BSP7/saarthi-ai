import logging
import os
import joblib
import pandas as pd

logger = logging.getLogger(__name__)

# Global cache for models so they are only loaded once per worker process
_models_cache = {}

def load_models():
    """Load and cache the trained ML models and feature names."""
    global _models_cache
    if _models_cache:
        return _models_cache
        
    base_dir = os.path.dirname(os.path.dirname(__file__))
    models_dir = os.path.join(base_dir, "ml_models")
    
    try:
        # Load Random Forest
        rf_path = os.path.join(models_dir, "random_forest_model.pkl")
        if os.path.exists(rf_path):
            _models_cache["random_forest"] = joblib.load(rf_path)
            
        # Load feature names
        features_path = os.path.join(models_dir, "feature_names.pkl")
        if os.path.exists(features_path):
            _models_cache["feature_names"] = joblib.load(features_path)
            
        logger.info("Successfully loaded ML models from disk.")
    except Exception as e:
        logger.error(f"Failed to load ML models: {e}")
        
    return _models_cache

def generate_recommendations(assessment_data: dict) -> list:
    """
    Generates top 3 career recommendations using the trained Random Forest model.
    Falls back to mock data if the model isn't available.
    """
    logger.info("Generating recommendations for assessment data")
    
    models = load_models()
    rf_model = models.get("random_forest")
    feature_names = models.get("feature_names")
    
    if not rf_model or not feature_names:
        logger.warning("ML models not found, falling back to mock recommendations.")
        return get_mock_recommendations()

    # Prepare input data
    # If a feature is missing from the assessment_data, default to 5
    input_features = {feature: assessment_data.get(feature, 5) for feature in feature_names}
    
    # Create DataFrame to match the format expected by scikit-learn
    df_input = pd.DataFrame([input_features])
    
    # Get probabilities for all classes
    probabilities = rf_model.predict_proba(df_input)[0]
    classes = rf_model.classes_
    
    # Combine classes with their probabilities
    career_probs = list(zip(classes, probabilities))
    
    # Sort by highest probability
    career_probs.sort(key=lambda x: x[1], reverse=True)
    
    # Take top 3
    top_3 = career_probs[:3]
    
    recommendations = []
    for i, (career_title, prob) in enumerate(top_3):
        score = int(prob * 100)
        recommendations.append({
            "career_id": f"c_{i+1}", # We use dummy IDs for now until DB integration
            "title": career_title,
            "match_score": score,
            "description": f"A great match based on your assessment scores.",
            "reason": f"Your profile strongly aligns with the {career_title} role."
        })
        
    return recommendations

def get_mock_recommendations():
    return [
        {
            "career_id": "c_001",
            "title": "Software Engineer",
            "match_score": 95,
            "description": "Develop and maintain software systems.",
            "reason": "Strong alignment with problem-solving and coding interests."
        },
        {
            "career_id": "c_002",
            "title": "Data Scientist",
            "match_score": 88,
            "description": "Analyze and interpret complex digital data.",
            "reason": "High interest in analytics and mathematical reasoning."
        },
        {
            "career_id": "c_003",
            "title": "Product Manager",
            "match_score": 75,
            "description": "Oversee the development and success of a product.",
            "reason": "Good balance of technical knowledge and leadership skills."
        }
    ]
