"""
LLM Service for Startup Business Guide

This service handles integration with Groq API to provide
accurate, free AI responses for startup business queries.
"""

import asyncio #just incase
import time
from typing import Optional, List
import logging
from groq import AsyncGroq
from config.settings import Settings


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMServiceError(Exception):
    """Custom exception for LLM service errors"""
    pass


class LLMService:
    """
    Service class for LLM integration using Groq API
    
    Provides free, accurate AI responses specifically tailored
    for startup business guidance and entrepreneurship questions.
    """
    
    def __init__(self, settings: Settings):
        """
        Initialize the LLM service
        
        Args:
            settings: Application settings containing Groq API configuration
        """
        self.settings = settings
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = settings.MODEL_NAME
        
        # Performance tracking
        self._total_requests = 0
        self._total_response_time = 0.0
        
        logger.info(f"LLM Service initialized with model: {self.model}")
    
    async def generate_response(
        self,
        question: str,
        context: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> dict:
        """
        Generate AI response for startup business questions
        
        Args:
            question: The user's question
            context: Optional additional context
            user_id: Optional user identifier for tracking
            
        Returns:
            Dictionary containing response, confidence, processing_time, etc.
            
        Raises:
            LLMServiceError: When LLM service fails to generate response
        """
        start_time = time.time()
        
        try:
            # Build the system prompt for startup business guidance
            system_prompt = self._build_system_prompt()
            
            # Build the user message with context if provided
            user_message = self._build_user_message(question, context)
            
            # Log the request
            logger.info(f"Processing question for user {user_id}: {question[:100]}...")
            
            # Call Groq API
            response = await self._call_groq_api(system_prompt, user_message)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Update performance metrics
            self._update_metrics(processing_time)
            
            # Build response dictionary
            result = {
                "answer": response.choices[0].message.content,
                "confidence": self._calculate_confidence(response),
                "processing_time": round(processing_time, 2),
                "model_used": self.model,
                "sources": self._extract_sources(response.choices[0].message.content),
            }
            
            logger.info(f"Response generated in {processing_time:.2f}s for user {user_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise LLMServiceError(f"Failed to generate response: {str(e)}")
    
    async def health_check(self) -> dict:
        """
        Check the health of the LLM service
        
        Returns:
            Dictionary with service health information
        """
        try:
            # Simple test query to verify connection
            test_response = await self._call_groq_api(
                "You are a helpful assistant.",
                "Respond with exactly: 'Health check successful'"
            )
            
            if test_response and test_response.choices:
                status = "connected"
            else:
                status = "disconnected"
            
            return {
                "status": status,
                "model": self.model,
                "total_requests": self._total_requests,
                "average_response_time": round(
                    self._total_response_time / max(self._total_requests, 1), 2
                )
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "disconnected",
                "error": str(e),
                "model": self.model
            }
    
    def _build_system_prompt(self) -> str:
        """
        Build the system prompt for startup business guidance
        
        Returns:
            Formatted system prompt string
        """
        return f"""
{self.settings.SYSTEM_PROMPT}

**Key Guidelines:**
- Provide accurate, actionable advice for entrepreneurs
- Include specific requirements, documents, or steps when applicable
- Mention regulatory considerations and legal requirements
- Suggest reliable sources or official websites when relevant
- Be comprehensive but concise
- Use bullet points and clear formatting for readability
- Focus on practical, implementable guidance

**Response Format:**
- Start with a direct answer
- Provide detailed steps or requirements
- Include important considerations or warnings
- End with additional resources if applicable
"""
    
    def _build_user_message(self, question: str, context: Optional[str] = None) -> str:
        """
        Build the user message with optional context
        
        Args:
            question: The main question
            context: Optional additional context
            
        Returns:
            Formatted user message string
        """
        if context:
            return f"""
**Context:** {context}

**Question:** {question}
"""
        return question
    
    async def _call_groq_api(self, system_prompt: str, user_message: str) -> any:
        """
        Make async call to Groq API
        
        Args:
            system_prompt: System prompt for the LLM
            user_message: User's message/question
            
        Returns:
            Groq API response object
            
        Raises:
            LLMServiceError: When API call fails
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,  # Balanced creativity and consistency
                max_tokens=2048,  # Sufficient for detailed responses
                top_p=0.9,       # High quality responses
                stream=False
            )
            return response
            
        except Exception as e:
            logger.error(f"Groq API call failed: {str(e)}")
            raise LLMServiceError(f"Groq API error: {str(e)}")
    
    def _calculate_confidence(self, response: any) -> float:
        """
        Calculate confidence score based on response characteristics
        
        Args:
            response: Groq API response object
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        # Base confidence from model performance
        base_confidence = 0.85
        
        # Adjust based on response length (longer responses often more detailed)
        content = response.choices[0].message.content
        length_factor = min(len(content) / 1000, 0.1)  # Up to 0.1 bonus
        
        # Check for specific indicators of good responses
        quality_indicators = [
            "required", "documents", "steps", "process", 
            "regulations", "official", "website", "contact"
        ]
        
        quality_score = sum(1 for indicator in quality_indicators 
                          if indicator.lower() in content.lower()) * 0.01
        
        final_confidence = min(base_confidence + length_factor + quality_score, 0.98)
        return round(final_confidence, 2)
    
    def _extract_sources(self, content: str) -> Optional[List[str]]:
        """
        Extract potential sources from the response content
        
        Args:
            content: Response content to analyze
            
        Returns:
            List of potential sources or None
        """
        # Common source indicators for startup business guidance
        source_patterns = [
            "Ministry", "Department", "Government", "Official",
            "Embassy", "Consulate", "Chamber of Commerce",
            "Registration Service", "Tax Authority", "Immigration"
        ]
        
        sources = []
        for pattern in source_patterns:
            if pattern.lower() in content.lower():
                sources.append(pattern)
        
        # Add some common reliable sources for startup guidance
        if "visa" in content.lower() or "travel" in content.lower():
            sources.extend(["Immigration Service", "Embassy"])
        
        if "business registration" in content.lower():
            sources.extend(["Business Registration Service", "Chamber of Commerce"])
        
        if "tax" in content.lower():
            sources.append("Tax Authority")
        
        return sources[:5] if sources else None  # Limit to 5 sources
    
    def _update_metrics(self, processing_time: float):
        """
        Update performance tracking metrics
        
        Args:
            processing_time: Time taken for this request
        """
        self._total_requests += 1
        self._total_response_time += processing_time
    
    def get_performance_stats(self) -> dict:
        """
        Get current performance statistics
        
        Returns:
            Dictionary with performance metrics
        """
        return {
            "total_requests": self._total_requests,
            "average_response_time": round(
                self._total_response_time / max(self._total_requests, 1), 2
            ),
            "model": self.model
        }


# Global service instance (will be initialized in main.py)
llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """
    Get the global LLM service instance
    
    Returns:
        LLM service instance
        
    Raises:
        RuntimeError: If service is not initialized
    """
    if llm_service is None:
        raise RuntimeError("LLM service not initialized")
    return llm_service
