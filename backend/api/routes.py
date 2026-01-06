from fastapi import APIRouter, HTTPException
from backend.api.schemas import AnalyzeRequest, AnalyzeResponse
from backend.services.instagram_service import parse_instagram_url
from backend.services.deepfake_service import analyze_deepfake
from backend.services.toxicity_service import analyze_toxicity
from backend.services.fusion_engine import fuse_results

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_instagram_post(payload: AnalyzeRequest):
    try:
        insta_data = parse_instagram_url(payload.instagram_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    deepfake_score = analyze_deepfake(insta_data)
    toxicity_score = analyze_toxicity(insta_data)
    risk = fuse_results(deepfake_score, toxicity_score)

    return AnalyzeResponse(
        deepfake_score=deepfake_score,
        toxicity_score=toxicity_score,
        risk_level=risk,
        message="AI analysis completed successfully"
    )
