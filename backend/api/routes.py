from fastapi import APIRouter
from backend.api.schemas import AnalyzeRequest, AnalyzeResponse

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_instagram_post(payload: AnalyzeRequest):
    deepfake_score = 0.82
    toxicity_score = 0.34

    if deepfake_score > 0.7 and toxicity_score > 0.3:
        risk = "High"
    elif deepfake_score > 0.7 or toxicity_score > 0.3:
        risk = "Medium"
    else:
        risk = "Low"

    return AnalyzeResponse(
        deepfake_score=deepfake_score,
        toxicity_score=toxicity_score,
        risk_level=risk,
        message="Mock analysis completed successfully"
    )
