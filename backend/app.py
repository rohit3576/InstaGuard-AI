from fastapi import FastAPI
from backend.api.routes import router as api_router

app = FastAPI(
    title="InstaGuard AI",
    description="Deepfake Detection & Toxic Comment Analysis for Instagram",
    version="1.0.0"
)

app.include_router(api_router)

@app.get("/")
def root():
    return {
        "status": "running",
        "project": "InstaGuard AI"
    }
