from typing import Dict
from transformers import pipeline
from backend.services.comment_service import fetch_instagram_comments

toxicity_classifier = pipeline(
    "text-classification",
    model="unitary/toxic-bert",
    tokenizer="unitary/toxic-bert",
    top_k=None
)


def analyze_toxicity(instagram_data: Dict) -> float:
    """
    Analyze toxicity of real Instagram comments.
    """

    shortcode = instagram_data["shortcode"]
    comments = fetch_instagram_comments(shortcode)

    if not comments:
        return 0.0

    results = toxicity_classifier(comments)

    toxic_scores = []

    for comment_result in results:
        for label in comment_result:
            if label["label"].lower() == "toxic":
                toxic_scores.append(label["score"])

    if not toxic_scores:
        return 0.0

    return round(sum(toxic_scores) / len(toxic_scores), 2)
