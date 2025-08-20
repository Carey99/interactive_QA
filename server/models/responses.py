"""
Response models for the Startup Business Guide API

These Pydantic models define the structure of API responses
ensuring consistent and well-documented outputs.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class QuestionResponse(BaseModel):
    """
    Response model for AI-generated answers
    
    Attributes:
        answer: The AI-generated response to the user's question
        confidence: Confidence score of the response (0.0 to 1.0)
        processing_time: Time taken to generate the response in seconds
        model_used: Name of the LLM model used for generation
        sources: Optional list of sources or references
        timestamp: When the response was generated
    """
    
    answer: str = Field(
        ...,
        description="The AI-generated answer to the user's question",
        example="""For travel from Kenya to Ireland, you need:

**Required Documents:**
- Valid Kenyan passport (must be valid for at least 6 months)
- Irish visa (required for Kenyan citizens)
- Return flight tickets
- Proof of accommodation in Ireland
- Proof of sufficient funds (bank statements)
- Travel insurance

**Visa Requirements:**
- Short-stay visa (C visa) for visits up to 90 days
- Apply at VFS Global center in Nairobi
- Processing time: 15-20 working days
- Fee: €60 for adults

**Additional Considerations:**
- Yellow fever vaccination certificate may be required
- Business invitation letter if attending conferences
- Check latest travel advisories before departure"""
    )
    
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score of the response",
        example=0.95
    )
    
    processing_time: float = Field(
        ...,
        gt=0,
        description="Time taken to generate response in seconds",
        example=1.23
    )
    
    model_used: str = Field(
        ...,
        description="LLM model used for generation",
        example="llama-3.1-8b-instant"
    )
    
    sources: Optional[List[str]] = Field(
        None,
        description="Optional list of sources or references",
        example=["Irish Immigration Service", "VFS Global", "Kenya Ministry of Foreign Affairs"]
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When the response was generated"
    )
    
    class Config:
        """Pydantic configuration"""
        protected_namespaces = ()  # Allow model_ prefix
        json_schema_extra = {
            "example": {
                "answer": "For travel from Kenya to Ireland, you need: [detailed response]",
                "confidence": 0.95,
                "processing_time": 1.23,
                "model_used": "llama-3.1-8b-instant",
                "sources": ["Irish Immigration Service", "VFS Global"],
                "timestamp": "2025-08-20T10:30:00"
            }
        }


class HealthResponse(BaseModel):
    """
    Response model for health check endpoint
    
    Attributes:
        status: Overall system health status
        message: Human-readable status message
        llm_service_status: Status of the LLM service connection
        version: API version
        timestamp: When the health check was performed
    """
    
    status: str = Field(
        ...,
        description="Overall system health status",
        example="healthy"
    )
    
    message: str = Field(
        ...,
        description="Human-readable status message",
        example="All systems operational"
    )
    
    llm_service_status: str = Field(
        ...,
        description="Status of the LLM service",
        example="connected"
    )
    
    version: str = Field(
        ...,
        description="API version",
        example="1.0.0"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When the health check was performed"
    )
    
    class Config:
        """Pydantic configuration"""
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "message": "All systems operational",
                "llm_service_status": "connected",
                "version": "1.0.0",
                "timestamp": "2025-08-20T10:30:00"
            }
        }


class ErrorResponse(BaseModel):
    """
    Response model for error responses
    
    Attributes:
        error: Error type or code
        message: Human-readable error message
        details: Optional additional error details
        timestamp: When the error occurred
    """
    
    error: str = Field(
        ...,
        description="Error type or code",
        example="validation_error"
    )
    
    message: str = Field(
        ...,
        description="Human-readable error message",
        example="The question field is required and cannot be empty"
    )
    
    details: Optional[dict] = Field(
        None,
        description="Optional additional error details",
        example={"field": "question", "constraint": "min_length"}
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When the error occurred"
    )
