from typing import Dict, List
from transformers import pipeline

# Load once (VERY IMPORTANT)
toxicity_classifier = pipeline(
    "text-classification",
    model="unitary/toxic-bert",
    tokenizer="unitary/toxic-bert",
    top_k=None
)



def analyze_toxicity(instagram_data: Dict) -> float:
    """
    Analyze toxicity of comments using DistilBERT.
    """

    # 🔹 Mock comments for now
    comments: List[str] = [
        "This is fake and stupid",
        "You are an idiot",
        "Nice video!"
    ]

    results = toxicity_classifier(comments)

    toxic_scores = []

    for comment_result in results:
        for label in comment_result:
            if label["label"].lower() == "toxic":
                toxic_scores.append(label["score"])

    if not toxic_scores:
        return 0.0

    return round(sum(toxic_scores) / len(toxic_scores), 2)
