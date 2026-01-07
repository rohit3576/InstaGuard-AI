from fastapi import APIRouter, HTTPException

from backend.api.schemas import AnalyzeRequest, AnalyzeResponse
from backend.services.instagram_service import parse_instagram_url
from backend.services.comment_service import fetch_instagram_comments
from backend.services.toxicity_service import analyze_toxicity
from backend.services.deepfake_service import analyze_video_deepfake
from backend.services.fusion_engine import fuse_results

router = APIRouter(prefix="/api", tags=["Analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_instagram_post(payload: AnalyzeRequest):
    """
    Analyze an Instagram post/reel for:
    - Toxic comments (text)
    - Deepfake likelihood (video)
    """

    # 1️⃣ Parse & validate Instagram URL
    try:
        insta_data = parse_instagram_url(str(payload.instagram_url))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 2️⃣ Fetch comments (safe + fallback)
    comments = fetch_instagram_comments(insta_data["shortcode"])

    # 3️⃣ Toxicity analysis (BERT)
    toxicity_result = analyze_toxicity(comments)

    # 4️⃣ Video deepfake analysis (baseline / stub)
    video_result = analyze_video_deepfake(insta_data["original_url"])

    # 5️⃣ Fuse results into final risk
    final_result = fuse_results(
        text_result=toxicity_result,
        video_result=video_result
    )

    # 6️⃣ API response
    return AnalyzeResponse(
        instagram=insta_data,
        toxicity=toxicity_result,
        deepfake=video_result,
        final_analysis=final_result,
        message="AI analysis completed successfully"
    )
