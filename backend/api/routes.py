from fastapi import APIRouter, HTTPException, UploadFile, File
from backend.api.schemas import AnalyzeRequest, AnalyzeResponse
from backend.services.instagram_service import parse_instagram_url
from backend.services.comment_service import fetch_instagram_comments
from backend.services.toxicity_service import analyze_toxicity
from backend.services.deepfake_service import analyze_video_deepfake
from backend.services.fusion_engine import fuse_results

router = APIRouter()


# ======================================================
# MODE B — VIDEO UPLOAD (FULL DEEPFAKE)
# ======================================================
@router.post("/api/analyze/video")
async def analyze_uploaded_video(video: UploadFile = File(...)):
    """
    Deepfake detection for uploaded videos only
    """

    if not video.filename.endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Only MP4 videos are supported")

    result = analyze_video_deepfake(video)

    return result


# ======================================================
# MODE A — INSTAGRAM URL (TEXT ONLY)
# ======================================================
@router.post("/api/analyze", response_model=AnalyzeResponse)
def analyze_instagram_post(payload: AnalyzeRequest):
    """
    Instagram analysis:
    - Toxic comments
    - Metadata
    - NO video processing
    """

    try:
        insta_data = parse_instagram_url(str(payload.instagram_url))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Fetch comments (safe + fallback)
    comments = fetch_instagram_comments(insta_data["shortcode"])

    # Toxicity analysis
    toxicity_score = analyze_toxicity(comments)

    # No video allowed → deepfake score fixed
    deepfake_score = 0.0

    # Fuse results
    risk_level = fuse_results(
        text_result=toxicity_score,
        video_result=None
    )

    return AnalyzeResponse(
        deepfake_score=deepfake_score,
        toxicity_score=toxicity_score["score"],
        risk_level=risk_level,
        message="Instagram text analysis completed"
    )
