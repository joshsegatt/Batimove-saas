"""
Batimove Backend API - Minimal Version for Debugging
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Batimove API",
    description="Backend API for Batimove",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Batimove API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/api")
async def api_root():
    return {
        "message": "Batimove API",
        "status": "ok"
    }

# For Vercel
handler = app
