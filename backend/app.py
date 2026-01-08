from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.routes import router as api_router

app = FastAPI(
    title="InstaGuard AI",
    description="Deepfake Detection & Toxic Comment Analysis for Instagram",
    version="1.0.0"
)

# --------------------------------------------------
# CORS CONFIG (frontend + future browser extension)
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# API ROUTES
# --------------------------------------------------
# NOTE:
# /api prefix is already defined inside routes.py
# DO NOT add prefix here again
app.include_router(api_router)

# --------------------------------------------------
# FRONTEND SERVING
# --------------------------------------------------
# frontend/index.html is served at "/"
app.mount(
    "/",
    StaticFiles(directory="frontend", html=True),
    name="frontend"
)
