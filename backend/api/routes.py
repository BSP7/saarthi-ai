from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from ai.recommendation import generate_recommendations

router = APIRouter()

class AssessmentData(BaseModel):
    user_id: str
    answers: Dict[str, Any]

@router.get("/health")
def health_check():
    return {"status": "ok", "service": "Saarthi AI API"}

@router.post("/recommendation/generate")
def get_recommendations(data: AssessmentData):
    """
    Generate career recommendations based on assessment data.
    This endpoint delegates to the AI models.
    """
    # Pass the assessment answers to our AI module
    recommendations = generate_recommendations(data.answers)
    
    return {
        "status": "success",
        "user_id": data.user_id,
        "recommendations": recommendations
    }
