"""
Request models for the Startup Business Guide API

These Pydantic models define the structure and validation
for incoming API requests.
"""

from pydantic import BaseModel, Field
from typing import Optional


class QuestionRequest(BaseModel):
    """
    Request model for submitting questions to the AI assistant
    
    Attributes:
        question: The user's question or query (required)
        context: Optional additional context for the question
        user_id: Optional user identifier for tracking
    """
    
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The question or query to ask the AI assistant",
        example="What documents do I need to travel from Kenya to Ireland for business?"
    )
    
    context: Optional[str] = Field(
        None,
        max_length=1000,
        description="Optional additional context to help answer the question",
        example="I'm planning to attend a startup conference and meet potential investors"
    )
    
    user_id: Optional[str] = Field(
        None,
        max_length=100,
        description="Optional user identifier for tracking purposes",
        example="user_12345"
    )
    
    class Config:
        """Pydantic configuration"""
        json_schema_extra = {
            "example": {
                "question": "What documents do I need to travel from Kenya to Ireland?",
                "context": "I'm a startup founder planning to attend a business conference",
                "user_id": "startup_founder_001"
            }
        }
