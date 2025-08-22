"""
Alternative main.py for Render deployment using HTTP-based LLM service

This version uses direct HTTP calls to avoid Rust compilation issues.
"""

import asyncio
import time
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

# Import our models and services
from config.settings import Settings
from models import QuestionRequest, QuestionResponse, HealthResponse, ErrorResponse
from services.llm_service_http import LLMServiceHTTP, get_llm_service, set_llm_service, LLMServiceError


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize settings
settings = Settings()

# Global LLM service instance
llm_service_instance = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    
    Handles startup and shutdown events for the FastAPI application.
    """
    global llm_service_instance
    
    # Startup
    logger.info("Starting Startup Business Guide API...")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Initialize LLM service
    try:
        llm_service_instance = LLMServiceHTTP(settings)
        set_llm_service(llm_service_instance)
        
        # Test the service
        health_ok = await llm_service_instance.check_health()
        if health_ok:
            logger.info("✅ LLM service initialized and healthy")
        else:
            logger.warning("⚠️ LLM service initialized but health check failed")
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize LLM service: {str(e)}")
        # Don't fail startup, but service will be unavailable
    
    yield
    
    # Shutdown
    logger.info("Shutting down Startup Business Guide API...")
    if llm_service_instance:
        await llm_service_instance.close()
    logger.info("Shutdown complete")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    AI-powered startup business guidance system using free Groq LLM.
    
    Get expert advice on:
    - Business strategy and market analysis
    - Product development and MVP planning  
    - Funding and financial planning
    - Operations and team building
    - Marketing and customer acquisition
    
    Perfect for entrepreneurs and startup founders looking for actionable insights.
    """,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/", response_model=dict)
async def root():
    """
    API root endpoint providing system information
    """
    return {
        "message": "🚀 Startup Business Guide API",
        "version": settings.APP_VERSION,
        "status": "operational",
        "description": "AI-powered startup business guidance",
        "endpoints": {
            "health": "/health",
            "ask": "/api/ask", 
            "stats": "/api/stats",
            "docs": "/docs"
        },
        "features": [
            "Free AI-powered responses using Groq LLM",
            "Startup business expertise",
            "Real-time health monitoring",
            "Performance statistics",
            "Interactive API documentation"
        ]
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    
    Returns system health status including LLM service connectivity
    """
    try:
        # Check LLM service health
        llm_service = get_llm_service()
        llm_healthy = await llm_service.check_health()
        
        return HealthResponse(
            status="healthy" if llm_healthy else "degraded",
            timestamp=datetime.now(),
            llm_status="connected" if llm_healthy else "disconnected",
            version=settings.APP_VERSION
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.now(),
            llm_status="error",
            version=settings.APP_VERSION,
            error=str(e)
        )


@app.post("/api/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Submit a question for AI-powered startup business guidance
    
    This endpoint processes business questions and returns expert advice
    specifically tailored for entrepreneurs and startup founders.
    """
    try:
        if not request.question or not request.question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )
        
        # Get LLM service
        llm_service = get_llm_service()
        
        # Process the question
        result = await llm_service.ask_question(request.question.strip())
        
        return QuestionResponse(
            response=result["response"],
            confidence=result["confidence"],
            response_time=result["response_time"],
            timestamp=datetime.now(),
            model=result["model"]
        )
        
    except LLMServiceError as e:
        logger.error(f"LLM service error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"AI service temporarily unavailable: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in ask_question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@app.get("/api/stats", response_model=dict)
async def get_statistics():
    """
    Get system performance statistics
    
    Returns metrics about API usage, response times, and system performance
    """
    try:
        llm_service = get_llm_service()
        stats = llm_service.get_statistics()
        
        return {
            "api_stats": stats,
            "system_info": {
                "version": settings.APP_VERSION,
                "model": settings.MODEL_NAME,
                "uptime": "Available via health endpoint"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        return {
            "error": "Statistics temporarily unavailable",
            "system_info": {
                "version": settings.APP_VERSION,
                "status": "degraded"
            }
        }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions with proper error responses"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected exceptions"""
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
