"""
FastAPI Backend for Startup Business Guide

This is the main entry point for the AI-powered Q&A system
specifically designed for startup business guidance and entrepreneurship.
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
from services import LLMService, get_llm_service, LLMServiceError


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
        llm_service_instance = LLMService(settings)
        # Update the global service reference
        import services.llm_service as llm_module
        llm_module.llm_service = llm_service_instance
        logger.info("LLM service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize LLM service: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Startup Business Guide API...")


# Create FastAPI application with custom configuration
app = FastAPI(
    title="Startup Business Guide API",
    description="""
    AI-powered Q&A system for startup business guidance and entrepreneurship.
    
    This API provides accurate, free responses to business-related questions using
    advanced language models. Perfect for entrepreneurs seeking guidance on:
    
    - Business registration and legal requirements
    - International travel and visa requirements
    - Regulatory compliance and documentation
    - Market research and business planning
    - Financial planning and funding options
    
    **Features:**
    - Free AI-powered responses using Groq LLM
    - Specialized prompts for startup business guidance
    - Comprehensive error handling and validation
    - Performance monitoring and health checks
    - Full Swagger UI documentation
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint - API information
    
    Returns basic information about the API and links to documentation.
    """
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
    """
    Health check endpoint
    
    Returns the current status of the API and its dependencies.
    This endpoint is used for monitoring and load balancer health checks.
    """
    try:
        llm_service = get_llm_service()
        llm_health = await llm_service.health_check()
        
        return HealthResponse(
            status="healthy",
            message="All systems operational",
            llm_service_status=llm_health["status"],
            version="1.0.0"
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="degraded",
            message=f"LLM service issue: {str(e)}",
            llm_service_status="disconnected",
            version="1.0.0"
        )


@app.post("/api/ask", response_model=QuestionResponse, tags=["Q&A"])
async def ask_question(request: QuestionRequest):
    """
    Ask a business-related question
    
    Submit a question related to startup business guidance and receive
    an AI-generated response with actionable advice and recommendations.
    
    **Example Questions:**
    - "What documents do I need to travel from Kenya to Ireland?"
    - "How do I register a business in the United States?"
    - "What are the visa requirements for attending a conference in Germany?"
    - "How do I open a business bank account in Canada?"
    
    **Response includes:**
    - Detailed answer with actionable steps
    - Confidence score of the response
    - Processing time and model information
    - Relevant sources and references
    """
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


@app.get("/api/stats", tags=["Monitoring"])
async def get_performance_stats():
    """
    Get API performance statistics
    
    Returns performance metrics for monitoring and optimization.
    """
    try:
        llm_service = get_llm_service()
        stats = llm_service.get_performance_stats()
        
        return {
            "api_version": "1.0.0",
            "llm_stats": stats,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "stats_error",
                "message": "Failed to retrieve performance statistics",
                "timestamp": datetime.now().isoformat()
            }
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Global HTTP exception handler
    
    Provides consistent error responses across the API.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "http_error",
            "message": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Global exception handler for unexpected errors
    
    Ensures that all errors are properly logged and return consistent responses.
    """
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred. Please try again.",
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
