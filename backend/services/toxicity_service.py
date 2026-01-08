from typing import List, Dict
from transformers import pipeline

# --------------------------------------------------
# LOAD MODEL ONCE (IMPORTANT FOR PERFORMANCE)
# --------------------------------------------------
toxicity_pipeline = pipeline(
    "text-classification",
    model="unitary/toxic-bert",
    top_k=None
)


def analyze_toxicity(comments: List[str]) -> Dict:
    """
    Analyze a list of comments and return an aggregated toxicity score.
    """

    # 🛡️ Safety: empty or invalid input
    if not comments:
        return {
            "toxicity_score": 0.0,
            "label": "UNKNOWN",
            "model": "unitary/toxic-bert"
        }

    scores = []

    for text in comments:
        try:
            result = toxicity_pipeline(text[:512])[0]
            toxic_score = next(
                (item["score"] for item in result if item["label"] == "toxic"),
                0.0
            )
            scores.append(toxic_score)
        except Exception:
            continue

    # If model failed on all comments
    if not scores:
        return {
            "toxicity_score": 0.0,
            "label": "UNKNOWN",
            "model": "unitary/toxic-bert"
        }

    avg_score = round(sum(scores) / len(scores), 2)

    return {
        "toxicity_score": avg_score,
        "label": "TOXIC" if avg_score > 0.5 else "NON_TOXIC",
        "model": "unitary/toxic-bert"
    }
