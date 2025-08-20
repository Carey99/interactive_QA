# LLM Prompts Documentation

This document contains all the prompts used with the LLM (Groq API with llama-3.1-8b-instant) in our Interactive Q&A System.

## System Architecture

The LLM integration is handled through the `LLMService` class in `server/services/llm_service.py`, which uses Groq's free API to provide intelligent startup business guidance.

## Primary System Prompt

**Location**: `server/services/llm_service.py` - `_get_system_prompt()` method

```
You are an expert startup business advisor with extensive knowledge in entrepreneurship, business strategy, market analysis, funding, product development, and scaling operations.

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

Always aim to help the user make informed decisions that will increase their startup's chances of success.
```

## Health Check Prompt

**Location**: `server/services/llm_service.py` - `check_health()` method

**User Message**: "Hello"

**Expected Response Pattern**: The system expects a successful response from the LLM to verify connectivity and proper API functioning.

## Prompt Engineering Strategy

### 1. **Persona Definition**
- **Role**: Expert startup business advisor
- **Expertise Areas**: Entrepreneurship, business strategy, market analysis, funding, product development, scaling
- **Tone**: Professional, encouraging, practical

### 2. **Response Structure Guidelines**
- **Conciseness**: Clear and direct communication
- **Actionability**: Specific steps and recommendations
- **Evidence-Based**: Include examples and case studies
- **Stage-Aware**: Consider startup maturity level
- **Balanced**: Encouraging yet realistic

### 3. **Content Focus Areas**
- Business Strategy & Market Analysis
- Product Development & MVP Creation
- Funding & Financial Planning
- Operations & Team Building
- Marketing & Customer Acquisition

### 4. **Response Enhancement Features**
- **Confidence Scoring**: Each response includes a confidence level (0.0-1.0)
- **Performance Tracking**: Response times and success rates monitored
- **Error Handling**: Graceful degradation with informative error messages

## Implementation Details

### LLM Configuration
- **Model**: `llama-3.1-8b-instant` (Groq)
- **API**: Groq AsyncClient
- **Rate Limiting**: Handled by Groq's free tier limits
- **Timeout**: Configurable timeout for API calls

### Prompt Flow
1. **System Prompt**: Loaded once during service initialization
2. **User Input**: Received through `/api/ask` endpoint
3. **Context Building**: User question combined with system prompt
4. **API Call**: Async call to Groq API
5. **Response Processing**: Parse and validate LLM response
6. **Confidence Scoring**: Assign confidence level based on response quality
7. **Return**: Formatted response with metadata

### Error Handling Prompts
- **API Failures**: "I'm currently experiencing technical difficulties. Please try again in a moment."
- **Invalid Responses**: "I couldn't process that request properly. Could you please rephrase your question?"
- **Rate Limiting**: "I'm currently at capacity. Please wait a moment before asking another question."

## Prompt Testing & Validation

### Health Check Validation
The system performs periodic health checks by sending a simple "Hello" message to ensure:
- API connectivity is maintained
- Response times are acceptable
- LLM is responding appropriately

### Response Quality Metrics
- **Response Time**: Tracked for performance monitoring
- **Success Rate**: Percentage of successful API calls
- **Confidence Levels**: Average confidence scores
- **Error Rates**: Monitoring of different error types

## Future Prompt Enhancements

### Planned Improvements
1. **Dynamic Prompt Adjustment**: Adapt prompts based on user's startup stage
2. **Context Awareness**: Maintain conversation context for follow-up questions
3. **Specialized Prompts**: Different prompts for different business areas
4. **Multilingual Support**: Prompts for different languages
5. **Industry-Specific Guidance**: Tailored prompts for different industry sectors

### A/B Testing Framework
- Test different prompt variations
- Measure response quality and user satisfaction
- Optimize for specific use cases and user feedback

---

*This documentation is part of the Interactive Q&A System assessment submission and demonstrates comprehensive prompt engineering for startup business guidance.*
