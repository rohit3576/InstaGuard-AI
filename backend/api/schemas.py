from pydantic import BaseModel, HttpUrl
from typing import Dict, Any, Optional


class AnalyzeRequest(BaseModel):
    instagram_url: HttpUrl


class AnalyzeResponse(BaseModel):
    instagram: Dict[str, Any]
    toxicity: Dict[str, Any]
    deepfake: Dict[str, Any]
    final_analysis: Dict[str, Any]
    message: Optional[str] = None
