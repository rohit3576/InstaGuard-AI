def fuse_results(text_result: dict, video_result: dict) -> dict:
    """
    Combine text toxicity + video deepfake risk.
    """

    text_score = text_result.get("toxicity_score", 0)
    video_score = video_result.get("deepfake_score", 0)

    final_score = round((text_score + video_score) / 2, 2)

    if final_score > 0.7:
        risk = "High"
    elif final_score > 0.4:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "final_risk": risk,
        "final_score": final_score,
        "text_score": text_score,
        "video_score": video_score
    }
