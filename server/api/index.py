"""
Vercel Handler for FastAPI Application

This module provides the ASGI application for Vercel's serverless deployment.
"""

from vercel_app import app

# Export the FastAPI app for Vercel
handler = app

# Also export as 'app' for compatibility
__all__ = ["app", "handler"]
