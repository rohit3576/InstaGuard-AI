from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.routes import router as api_router

# --------------------------------------------------
# FASTAPI APP (DOCS DISABLED — FRONTEND IS THE APP)
# --------------------------------------------------
app = FastAPI(
    title="InstaGuard AI",
    docs_url=None,        # ❌ disable /docs
    redoc_url=None,       # ❌ disable /redoc
    openapi_url=None      # ❌ disable /openapi.json
)

# --------------------------------------------------
# CORS CONFIG
# (frontend + future browser extension)
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # OK for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# API ROUTES
# --------------------------------------------------
# IMPORTANT:
# routes.py already uses prefix="/api"
# DO NOT add another prefix here
app.include_router(api_router)

# --------------------------------------------------
# FRONTEND SERVING (THE PRODUCT UI)
# --------------------------------------------------
# frontend/index.html will be served at "/"
app.mount(
    "/",
    StaticFiles(directory="frontend", html=True),
    name="frontend"
)
