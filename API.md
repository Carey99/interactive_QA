# API Documentation

## Overview
The Interactive Q&A System provides a RESTful API for startup business guidance powered by AI.

## Base URL
```
http://localhost:8001
```

## Authentication
Currently no authentication required. API key protection is handled internally.

## Endpoints

### GET /health
Health check endpoint that verifies system status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-21T10:00:00Z",
  "llm_status": "connected"
}
```

### POST /api/ask
Submit a question for AI-powered response.

**Request:**
```json
{
  "question": "How do I validate my startup idea?"
}
```

**Response:**
```json
{
  "response": "To validate your startup idea...",
  "confidence": 0.95,
  "timestamp": "2025-08-21T10:00:00Z"
}
```

### GET /api/stats
Get system performance statistics.

**Response:**
```json
{
  "total_questions": 42,
  "avg_response_time": 1.5,
  "success_rate": 0.98
}
```
