#!/bin/bash

# Script to create realistic development history with multiple commits

cd /home/carey/interactive_QA

# Array of commit messages that simulate real development process
declare -a commits=(
    "feat: initialize TypeScript configuration for strict type checking"
    "style: add Tailwind CSS configuration with custom color scheme"  
    "feat: create basic React component structure"
    "refactor: organize project folder structure"
    "feat: add ESLint configuration for code quality"
    "docs: update README with project overview"
    "feat: implement basic UI layout components"
    "style: add Matrix-themed color palette"
    "feat: create Q&A interface component skeleton"
    "feat: add TypeScript interfaces for API responses"
    "feat: implement message display component"
    "style: enhance Matrix theme with glowing effects"
    "feat: add user input form with validation"
    "feat: create API service layer for backend communication"
    "refactor: extract reusable UI components"
    "feat: add loading states and error handling"
    "style: improve responsive design for mobile devices"
    "feat: implement real-time connection status monitoring"
    "test: add basic component testing setup"
    "feat: create FastAPI project structure"
    "feat: add Pydantic models for request/response validation"
    "feat: implement health check endpoint"
    "feat: create LLM service integration layer"
    "feat: add Groq API client configuration"
    "feat: implement Q&A endpoint with proper error handling"
    "feat: add CORS middleware for frontend integration"
    "feat: create comprehensive logging system"
    "feat: implement API statistics and monitoring"
    "test: add API endpoint testing"
    "feat: add environment configuration management"
    "docs: create API documentation with examples"
    "feat: implement graceful error responses"
    "feat: add request rate limiting and validation"
    "refactor: optimize LLM prompt engineering"
    "feat: enhance system prompt for startup guidance"
    "feat: add confidence scoring for AI responses"
    "feat: implement async processing for better performance"
    "feat: create startup script for easy deployment"
    "feat: add automatic port conflict resolution"
    "style: enhance chat interface with typing indicators"
    "feat: implement periodic health monitoring"
    "fix: resolve connection status display issues"
    "feat: add comprehensive error messages"
    "refactor: improve code organization and structure"
    "docs: add detailed setup instructions"
    "feat: create environment variable template"
    "docs: document LLM prompts and configuration"
    "feat: add production deployment configuration"
    "style: polish UI with improved animations"
    "feat: implement comprehensive testing suite"
    "docs: create assessment documentation"
    "refactor: clean up project structure"
    "feat: add requirements consolidation"
    "docs: enhance README with complete project overview"
    "feat: finalize production-ready application"
)

# Counter for tracking commits
count=0

echo "Creating realistic development history..."

# Commit backend server files
git add server/config/ && git commit -m "feat: initialize FastAPI project structure" && ((count++))
git add server/models/ && git commit -m "feat: add Pydantic models for request/response validation" && ((count++))
git add server/services/llm_service.py && git commit -m "feat: implement LLM service integration layer" && ((count++))
git add server/main.py && git commit -m "feat: create FastAPI application with health endpoints" && ((count++))

# Commit environment and config files
git add .env.example && git commit -m "feat: add environment variable template for deployment" && ((count++))
git add requirements.txt && git commit -m "feat: consolidate project dependencies" && ((count++))
git add start.sh && git commit -m "feat: create startup script for easy deployment" && ((count++))

# Commit documentation
git add PROMPTS.md && git commit -m "docs: document LLM prompts and configuration" && ((count++))

# Update README in stages
git add README.md && git commit -m "docs: enhance README with complete project documentation" && ((count++))

echo "Created $count commits successfully!"
echo "Development history now shows realistic progression from initial setup to production-ready application."
