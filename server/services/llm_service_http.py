"""
Alternative LLM Service using direct HTTP calls to Groq API

This version avoids the groq package to prevent Rust compilation issues
on Render deployment while maintaining the same functionality.
"""

import asyncio
import time
import json
from typing import Optional, Dict, Any
import logging
import httpx
from config.settings import Settings


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMServiceError(Exception):
    """Custom exception for LLM service errors"""
    pass


class LLMServiceHTTP:
    """
    Alternative LLM Service using direct HTTP calls to Groq API
    
    Provides the same functionality as the original LLMService
    but uses httpx for HTTP calls instead of the groq package.
    """
    
    def __init__(self, settings: Settings):
        """Initialize the LLM service with HTTP client"""
        self.settings = settings
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.MODEL_NAME
        self.base_url = "https://api.groq.com/openai/v1"
        
        # HTTP client configuration
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
        
        # Performance tracking
        self._total_requests = 0
        self._total_response_time = 0.0
        
        logger.info(f"HTTP LLM Service initialized with model: {self.model}")
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for startup business guidance"""
        return """You are an expert startup business advisor with extensive knowledge in entrepreneurship, business strategy, market analysis, funding, product development, and scaling operations.

Your role is to provide practical, actionable advice to entrepreneurs and startup founders. Focus on:

1. **Business Strategy**: Market analysis, competitive positioning, business model validation
2. **Product Development**: MVP strategies, user research, product-market fit
3. **Funding & Finance**: Fundraising strategies, financial planning, investor relations
4. **Operations & Scaling**: Team building, operational efficiency, growth strategies
5. **Marketing & Sales**: Customer acquisition, digital marketing, sales processes

Guidelines for responses:
- Be concise but comprehensive
- Provide actionable steps when possible
- Include relevant examples or case studies
- Consider the startup's stage (idea, MVP, growth, scaling)
- Be encouraging while being realistic about challenges
- Focus on data-driven decision making

Always aim to help the user make informed decisions that will increase their startup's chances of success."""

    async def ask_question(self, question: str) -> Dict[str, Any]:
        """
        Process a question and return an AI response
        
        Args:
            question: The user's question about startup business
            
        Returns:
            Dictionary containing response, confidence, and metadata
        """
        start_time = time.time()
        
        try:
            # Prepare the request payload
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": question}
                ],
                "max_tokens": self.settings.MAX_TOKENS,
                "temperature": self.settings.TEMPERATURE,
                "stream": False
            }
            
            # Make the API call
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract the response content
            ai_response = result["choices"][0]["message"]["content"]
            
            # Calculate confidence score based on response quality
            confidence = self._calculate_confidence(ai_response, question)
            
            # Update performance metrics
            response_time = time.time() - start_time
            self._total_requests += 1
            self._total_response_time += response_time
            
            logger.info(f"Question processed successfully in {response_time:.2f}s")
            
            return {
                "response": ai_response,
                "confidence": confidence,
                "response_time": response_time,
                "model": self.model,
                "timestamp": time.time()
            }
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from Groq API: {e.response.status_code} - {e.response.text}")
            raise LLMServiceError(f"API request failed: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            raise LLMServiceError(f"Network error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in ask_question: {str(e)}")
            raise LLMServiceError(f"Service error: {str(e)}")

    async def check_health(self) -> bool:
        """
        Check if the LLM service is healthy and responsive
        
        Returns:
            True if service is healthy, False otherwise
        """
        try:
            # Simple test call to verify API connectivity
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": "Hello"}
                ],
                "max_tokens": 10,
                "temperature": 0.1
            }
            
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload
            )
            
            response.raise_for_status()
            logger.info("LLM service health check passed")
            return True
            
        except Exception as e:
            logger.error(f"LLM service health check failed: {str(e)}")
            return False

    def _calculate_confidence(self, response: str, question: str) -> float:
        """Calculate confidence score for the response"""
        if not response or len(response.strip()) < 10:
            return 0.3
        
        # Basic confidence calculation
        confidence = 0.8
        
        # Boost confidence for longer, detailed responses
        if len(response) > 200:
            confidence += 0.1
        
        # Boost for structured responses
        if any(marker in response for marker in ['1.', '2.', '•', '-', 'Step']):
            confidence += 0.05
        
        return min(confidence, 1.0)

    def get_statistics(self) -> Dict[str, Any]:
        """Get service performance statistics"""
        avg_response_time = (
            self._total_response_time / self._total_requests 
            if self._total_requests > 0 else 0
        )
        
        return {
            "total_requests": self._total_requests,
            "average_response_time": round(avg_response_time, 2),
            "model": self.model,
            "service_type": "HTTP"
        }

    async def close(self):
        """Clean up resources"""
        await self.client.aclose()
        logger.info("LLM service HTTP client closed")


# Global service instance
_llm_service_instance = None


def get_llm_service() -> LLMServiceHTTP:
    """Get the global LLM service instance"""
    global _llm_service_instance
    if _llm_service_instance is None:
        raise RuntimeError("LLM service not initialized")
    return _llm_service_instance


def set_llm_service(service: LLMServiceHTTP):
    """Set the global LLM service instance"""
    global _llm_service_instance
    _llm_service_instance = service
