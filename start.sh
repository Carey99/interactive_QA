#!/bin/bash

# Interactive Q&A System Startup Script
# Starts both frontend and backend simultaneously

echo "🚀 Starting Interactive Q&A System..."
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -d "client" ] || [ ! -d "server" ]; then
    echo -e "${RED}❌ Error: Please run this script from the interactive_QA root directory${NC}"
    echo "Expected structure: interactive_QA/client and interactive_QA/server"
    exit 1
fi

# Check and kill existing processes on the ports we need
echo -e "${YELLOW}🔍 Checking for existing processes...${NC}"

# Kill any existing processes on port 8001 (backend)
EXISTING_BACKEND=$(lsof -ti :8001)
if [ ! -z "$EXISTING_BACKEND" ]; then
    echo -e "${YELLOW}⚠️  Killing existing backend process on port 8001${NC}"
    kill $EXISTING_BACKEND 2>/dev/null
    sleep 2
fi

# Kill any existing processes on port 3000 (frontend)
EXISTING_FRONTEND=$(lsof -ti :3000)
if [ ! -z "$EXISTING_FRONTEND" ]; then
    echo -e "${YELLOW}⚠️  Killing existing frontend process on port 3000${NC}"
    kill $EXISTING_FRONTEND 2>/dev/null
    sleep 2
fi

# Function to cleanup background processes
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down services...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}✅ Cleanup complete${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup SIGINT

echo -e "${BLUE}📦 Starting Backend Server...${NC}"
cd server

# Activate virtual environment and start backend
source ../.venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8001 > ../backend.log 2>&1 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${GREEN}✅ Backend server started (PID: $BACKEND_PID)${NC}"
    echo -e "   📍 API: http://localhost:8001"
    echo -e "   📚 Docs: http://localhost:8001/docs"
else
    echo -e "${RED}❌ Failed to start backend server${NC}"
    echo "Check backend.log for details"
    exit 1
fi

echo -e "${BLUE}🌐 Starting Frontend Server...${NC}"
cd ../client

# Start frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait a moment for frontend to start
sleep 5

# Check if frontend started successfully
if kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${GREEN}✅ Frontend server started (PID: $FRONTEND_PID)${NC}"
    echo -e "   🌐 App: http://localhost:3000"
else
    echo -e "${RED}❌ Failed to start frontend server${NC}"
    echo "Check frontend.log for details"
    cleanup
fi

echo ""
echo -e "${GREEN}🎉 Both services are running!${NC}"
echo "=================================="
echo -e "${BLUE}📱 Frontend:${NC} http://localhost:3000"
echo -e "${BLUE}🔧 Backend API:${NC} http://localhost:8001" 
echo -e "${BLUE}📖 API Docs:${NC} http://localhost:8001/docs"
echo ""
echo -e "${YELLOW}💡 Tips:${NC}"
echo "• Visit http://localhost:3000 to use the Q&A interface"
echo "• Visit http://localhost:8001/docs to test the API directly"
echo "• Check backend.log and frontend.log for detailed logs"
echo "• Press Ctrl+C to stop both services"
echo ""
echo -e "${GREEN}✨ Ready to answer your startup business questions!${NC}"

# Keep script running and wait for user to stop
wait $BACKEND_PID $FRONTEND_PID
