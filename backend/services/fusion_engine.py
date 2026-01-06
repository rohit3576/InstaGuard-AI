def fuse_results(deepfake_score: float, toxicity_score: float) -> str:
    """
    Combine deepfake & toxicity scores into final risk level.
    """

    if deepfake_score > 0.7 and toxicity_score > 0.3:
        return "High"
    elif deepfake_score > 0.7 or toxicity_score > 0.3:
        return "Medium"
    return "Low"
