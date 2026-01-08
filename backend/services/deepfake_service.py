import tempfile
import requests
import numpy as np
from typing import Dict

from backend.services.video_utils import extract_frames
from backend.services.deepfake_model import predict_frame


def analyze_video_deepfake(video_url: str) -> Dict:
    """
    CNN-based deepfake analysis.
    - Works for direct video URLs (.mp4)
    - Gracefully skips Instagram protected videos
    """

    # 1️⃣ Detect Instagram page URLs (NOT direct video)
    if "instagram.com" in video_url and not video_url.endswith(".mp4"):
        return {
            "deepfake_score": 0.0,
            "risk_level": "Unavailable",
            "model": "resnet18-face-cnn",
            "frames_analyzed": 0,
            "status": "instagram_video_protected",
            "note": "Instagram blocks direct video download. Upload-based analysis supported."
        }

    try:
        # 2️⃣ Download direct video
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=True) as tmp:
            r = requests.get(video_url, timeout=20)
            r.raise_for_status()
            tmp.write(r.content)
            tmp.flush()

            frames = extract_frames(tmp.name)

        if not frames:
            raise RuntimeError("No frames extracted from video")

        # 3️⃣ CNN inference
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
            "model": "resnet18-face-cnn",
            "frames_analyzed": len(scores),
            "status": "success"
        }

    except Exception as e:
        print(f"[INFO] Video analysis failed: {e}")
        return {
            "deepfake_score": 0.0,
            "risk_level": "Unknown",
            "model": "resnet18-face-cnn",
            "frames_analyzed": 0,
            "status": "failed"
        }
