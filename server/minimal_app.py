"""
Minimal FastAPI app for Vercel serverless deployment
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Create minimal FastAPI app
app = FastAPI(title="Startup Business Guide API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Backend is working!",
        "timestamp": datetime.now().isoformat(),
        "status": "healthy"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "message": "Backend is running",
        "timestamp": datetime.now().isoformat()
    }

# Export for Vercel
handler = app
