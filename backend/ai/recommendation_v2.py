import os
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Global cache for the model and dataset
_model = None
_feature_names = None
_dataset = None
_features_matrix = None

def load_resources():
    global _model, _feature_names, _dataset, _features_matrix
    base_dir = os.path.dirname(os.path.dirname(__file__))
    
    if _model is None:
        model_path = os.path.join(base_dir, "ml_models", "domain_classifier_rf.pkl")
        if os.path.exists(model_path):
            _model = joblib.load(model_path)
            
    if _feature_names is None:
        feat_path = os.path.join(base_dir, "ml_models", "feature_names_v2.pkl")
        if os.path.exists(feat_path):
            _feature_names = joblib.load(feat_path)
            
    if _dataset is None:
        data_path = os.path.join(base_dir, "ai", "careers_dataset_v2.csv")
        if os.path.exists(data_path):
            # We want unique occupations (drop the jitter rows for recommendation)
            df = pd.read_csv(data_path)
            # Remove jitter duplicates by grouping by soc_code and taking mean of features
            # Wait, easier to just drop duplicates on soc_code since base is first
            _dataset = df.drop_duplicates(subset=['soc_code']).reset_index(drop=True)
            if _feature_names:
                _features_matrix = _dataset[_feature_names].values

def generate_recommendations_v2(user_features: dict) -> dict:
    """
    Two-stage recommendation pipeline.
    1. Predict top 3 domains.
    2. Cosine similarity matching for top 5 occupations.
    """
    load_resources()
    
    if not _model or not _feature_names or _dataset is None:
        return {"error": "AI resources not fully trained or loaded."}
        
    # Build user vector exactly matching the model's expected feature order
    user_vector = []
    for feat in _feature_names:
        # Default to 5 if a feature is missing
        user_vector.append(float(user_features.get(feat, 5.0)))
        
    user_vector_np = np.array(user_vector).reshape(1, -1)
    
    # Stage 1: Predict Top 3 Domains
    # Get class probabilities
    proba = _model.predict_proba(user_vector_np)[0]
    classes = _model.classes_
    
    # Sort indices descending by probability
    top_indices = np.argsort(proba)[::-1][:3]
    top_domains = [classes[i] for i in top_indices]
    
    # Stage 2: Cosine Similarity Matching within Top 3 Domains
    # Filter dataset for those domains
    domain_mask = _dataset['target_domain'].isin(top_domains)
    filtered_df = _dataset[domain_mask].copy()
    
    if filtered_df.empty:
        return {"error": "No occupations found in predicted domains."}
        
    filtered_features = filtered_df[_feature_names].values
    
    # Calculate Cosine Similarity
    similarities = cosine_similarity(user_vector_np, filtered_features)[0]
    filtered_df['similarity_score'] = similarities
    
    # Get top 5
    top_occupations = filtered_df.sort_values(by='similarity_score', ascending=False).head(5)
    
    results = {
        "top_domains": top_domains,
        "recommendations": []
    }
    
    for _, row in top_occupations.iterrows():
        results["recommendations"].append({
            "soc_code": row["soc_code"],
            "title": row["occupation_title"],
            "domain": row["target_domain"],
            "description": row.get("description", ""),
            "match_score": round(row["similarity_score"] * 100, 1) # percentage
        })
        
    return results
