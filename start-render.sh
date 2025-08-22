# Start script for Render deployment
#!/bin/bash

echo "Starting Interactive Q&A System..."

# Start the FastAPI backend
cd server
python -m uvicorn main:app --host 0.0.0.0 --port $PORT
