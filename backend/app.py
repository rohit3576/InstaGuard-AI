from fastapi import FastAPI

app = FastAPI(
    title="InstaGuard AI",
    description="Deepfake Detection & Toxic Comment Analysis for Instagram",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "status": "running",
        "project": "InstaGuard AI"
    }
