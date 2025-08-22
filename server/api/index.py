from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.parse
from datetime import datetime

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
                
                # Simple AI response (placeholder)
                response = {
                    "answer": f"Thank you for your question: '{question}'. This is a placeholder response. The AI service will be integrated soon.",
                    "confidence": 0.8,
                    "model": "placeholder",
                    "processing_time": 0.1,
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
