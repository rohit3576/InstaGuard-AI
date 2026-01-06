from fastapi import APIRouter, HTTPException
from backend.api.schemas import AnalyzeRequest, AnalyzeResponse
from backend.services.instagram_service import parse_instagram_url

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_instagram_post(payload: AnalyzeRequest):
    try:
        insta_data = parse_instagram_url(payload.instagram_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 🔮 Mock AI logic (temporary)
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
        message=f"Analyzed Instagram {insta_data['content_type']} successfully"
    )
