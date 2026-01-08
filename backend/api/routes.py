from fastapi import APIRouter, HTTPException, UploadFile, File
import tempfile
import os

from backend.services.video_utils import extract_frames
from backend.services.face_utils import extract_faces
from backend.services.deepfake_model import predict_frame
import numpy as np

router = APIRouter(prefix="/api", tags=["Analysis"])


@router.post("/analyze/video")
def analyze_uploaded_video(file: UploadFile = File(...)):
    """
    Analyze user-uploaded video for deepfake detection.
    """

    if not file.filename.endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Only .mp4 videos are supported")

    try:
        # 1️⃣ Save uploaded video to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(file.file.read())
            video_path = tmp.name

        # 2️⃣ Extract frames
        frames = extract_frames(video_path)

        if not frames:
            raise RuntimeError("No frames extracted from uploaded video")

        face_scores = []

        # 3️⃣ Face detection + CNN
        for frame in frames:
            faces = extract_faces(frame)
            for face in faces:
                score = predict_frame(face)
                face_scores.append(score)

        if not face_scores:
            raise RuntimeError("No faces detected in video")

        avg_score = float(np.mean(face_scores))

        risk = (
            "High" if avg_score > 0.7
            else "Medium" if avg_score > 0.4
            else "Low"
        )

        return {
            "deepfake_score": round(avg_score, 2),
            "risk_level": risk,
            "model": "resnet18-face-cnn",
            "faces_analyzed": len(face_scores),
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Cleanup temp file
        if os.path.exists(video_path):
            os.remove(video_path)
