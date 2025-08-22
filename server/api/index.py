from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.parse
from datetime import datetime
import time

# Groq API integration
def call_groq_api(question):
    """Call Groq API for AI responses"""
    try:
        import requests
        
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return {
                "answer": "AI service is not configured. Please check the GROQ_API_KEY environment variable.",
                "confidence": 0,
                "error": "missing_api_key"
            }
        
        # Groq API endpoint
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # System prompt for startup business guidance
        system_prompt = """You are an expert startup business advisor and guide. Your role is to provide accurate, helpful, and actionable advice for entrepreneurs and startup founders.

Key areas of expertise:
- Business plan development
- Legal requirements and documentation
- Funding and investment strategies  
- Market research and validation
- Regulatory compliance
- International business and travel requirements
- Financial planning and management
- Team building and operations

Guidelines:
- Provide specific, actionable advice
- Include relevant documentation requirements when applicable
- Mention important deadlines or time-sensitive considerations
- Suggest reliable sources for additional information
- Be comprehensive but concise
- Use clear, professional language
- Structure responses with bullet points or numbered lists when helpful

Always aim to give practical, implementable guidance that helps users take concrete next steps."""

        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        start_time = time.time()
        response = requests.post(url, headers=headers, json=data, timeout=30)
        processing_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content']
            
            return {
                "answer": answer,
                "confidence": 0.9,
                "model": "llama-3.1-8b-instant",
                "processing_time": round(processing_time, 2)
            }
        else:
            return {
                "answer": f"Sorry, I encountered an error while processing your question. The AI service returned: {response.status_code}",
                "confidence": 0,
                "error": f"api_error_{response.status_code}"
            }
            
    except ImportError:
        return {
            "answer": "AI service dependencies not available. Using fallback response.",
            "confidence": 0,
            "error": "missing_dependencies"
        }
    except Exception as e:
        return {
            "answer": f"Sorry, I encountered an error: {str(e)}",
            "confidence": 0,
            "error": "processing_error"
        }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Add CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
        
        # Route handling
        if self.path == '/health':
            response = {
                "status": "healthy",
                "message": "Backend is running",
                "llm_service_status": "connected" if os.getenv('GROQ_API_KEY') else "disconnected",
                "version": "1.0.0",
                "timestamp": datetime.now().isoformat()
            }
        else:
            response = {
                "message": "Welcome to Startup Business Guide API",
                "description": "AI-powered Q&A system for entrepreneurs",
                "version": "1.0.0",
                "docs": "/docs",
                "health": "/health",
                "ask": "/api/ask"
            }
        
        self.wfile.write(json.dumps(response).encode())
        return

    def do_POST(self):
        # Add CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
        
        if self.path == '/api/ask':
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                request_data = json.loads(post_data.decode('utf-8'))
                question = request_data.get('question', '')
                
                if not question:
                    response = {
                        "error": "No question provided",
                        "message": "Please provide a question in the request body",
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    # Call Groq API for real AI response
                    ai_response = call_groq_api(question)
                    response = {
                        **ai_response,
                        "timestamp": datetime.now().isoformat()
                    }
                
            except Exception as e:
                response = {
                    "error": "Failed to process request",
                    "message": str(e),
                    "timestamp": datetime.now().isoformat()
                }
        else:
            response = {"error": "Endpoint not found"}
        
        self.wfile.write(json.dumps(response).encode())
        return

    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
        return
