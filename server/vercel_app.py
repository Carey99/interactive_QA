"""
Vercel-optimized FastAPI Backend for Startup Business Guide

This is a serverless-friendly version of the main FastAPI application
specifically configured for Vercel deployment.
"""

import time
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

# Import our models and services
from config.settings import Settings
from models import QuestionRequest, QuestionResponse, HealthResponse
from services import LLMService, LLMServiceError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize settings
settings = Settings()

# Create FastAPI app without lifespan for serverless
app = FastAPI(
    title="Startup Business Guide API",
    description="""
    AI-powered Q&A system for entrepreneurs and startup founders.
    
    This API provides expert guidance on:
    - Business registration and legal requirements
    - Travel and visa documentation
    - International business expansion
    - Financial planning and compliance
    - Market research and validation
    
    Features:
    - Free AI-powered responses using Groq LLM
    - Specialized prompts for startup business guidance
    - Comprehensive error handling and validation
    - Performance monitoring and health checks
    - Full Swagger UI documentation
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Initialize LLM service (lazy loading for serverless)
_llm_service = None

def get_llm_service():
    """Get or create LLM service instance"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService(settings)
    return _llm_service


@app.get("/", tags=["Root"])
async def read_root():
    """Root endpoint - API information"""
    return {
        "message": "Welcome to Startup Business Guide API",
        "description": "AI-powered Q&A system for entrepreneurs",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "ask": "/api/ask"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    try:
        llm_service = get_llm_service()
        llm_health = await llm_service.health_check()
        
        return HealthResponse(
            status="healthy",
            message="All systems operational",
            llm_service_status=llm_health["status"],
            version="1.0.0",
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="degraded",
            message=f"LLM service issue: {str(e)}",
            llm_service_status="disconnected",
            version="1.0.0",
            timestamp=datetime.now()
        )


@app.post("/api/ask", response_model=QuestionResponse, tags=["Q&A"])
async def ask_question(request: QuestionRequest):
    """Ask a business-related question"""
    try:
        llm_service = get_llm_service()
        
        # Generate response using LLM service
        response_data = await llm_service.generate_response(
            question=request.question,
            context=request.context,
            user_id=request.user_id
        )
        
        # Return structured response
        return QuestionResponse(**response_data)
        
    except LLMServiceError as e:
        logger.error(f"LLM service error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "llm_service_error",
                "message": "The AI service is temporarily unavailable. Please try again.",
                "timestamp": datetime.now().isoformat()
            }
        )
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_server_error",
                "message": "Failed to process your question. Please try again.",
                "timestamp": datetime.now().isoformat()
            }
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected exceptions"""
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred. Please try again.",
            "timestamp": datetime.now().isoformat()
        }
    )

# Export for Vercel
handler = app
