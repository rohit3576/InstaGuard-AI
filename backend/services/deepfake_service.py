import tempfile
import numpy as np
from typing import Dict
from backend.services.video_utils import extract_frames
from backend.services.deepfake_model import predict_frame


def analyze_video_deepfake(video_file) -> Dict:
    """
    Real CNN-based deepfake analysis (uploaded video)
    """

    try:
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            tmp.write(video_file.file.read())
            video_path = tmp.name

        frames = extract_frames(video_path)

        if not frames:
            raise RuntimeError("No frames extracted")

        scores = [predict_frame(f) for f in frames]
        avg_score = float(np.mean(scores))

        risk = (
            "High" if avg_score > 0.7
            else "Medium" if avg_score > 0.4
            else "Low"
        )

        return {
            "deepfake_score": round(avg_score, 2),
            "risk_level": risk,
            "frames_analyzed": len(scores),
            "status": "success"
        }

    except Exception as e:
        print(f"[ERROR] Video analysis failed: {e}")
        return {
            "deepfake_score": 0.0,
            "risk_level": "Unknown",
            "frames_analyzed": 0,
            "status": "failed"
        }
