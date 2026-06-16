from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok", "service": "Saarthi AI API"}

# --- V2 API for 30-feature Two-Stage Architecture ---

from ai.recommendation_v2 import generate_recommendations_v2

class AssessmentDataV2(BaseModel):
    user_id: str
    features: Dict[str, float]

@router.post("/v2/recommendation/generate")
def get_recommendations_v2(data: AssessmentDataV2):
    """
    Generate career recommendations using the V2 architecture.
    Expects exactly 30 features and returns Top 3 Domains + Top 5 Occupations using Cosine Similarity.
    """
    results = generate_recommendations_v2(data.features)
    
    return {
        "status": "success" if "error" not in results else "error",
        "user_id": data.user_id,
        "results": results
    }
