from pydantic import BaseModel, HttpUrl
from typing import Optional


class AnalyzeRequest(BaseModel):
    instagram_url: HttpUrl


class AnalyzeResponse(BaseModel):
    deepfake_score: float
    toxicity_score: float
    risk_level: str
    message: Optional[str] = None
