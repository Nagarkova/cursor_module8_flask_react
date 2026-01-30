#!/bin/bash

# Full-Stack Application Startup Script
# Starts both Flask backend and React frontend

echo "=========================================="
echo "Starting Full-Stack E-Commerce App"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    cd backend
    python3 -m venv venv
    cd ..
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source backend/venv/bin/activate

# Install backend dependencies
echo -e "${BLUE}Installing backend dependencies...${NC}"
cd backend
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
cd ..

# Install frontend dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${BLUE}Installing frontend dependencies...${NC}"
    cd frontend
    npm install > /dev/null 2>&1
    cd ..
fi

# Start backend server
echo -e "${GREEN}Starting Flask backend server on http://localhost:5001...${NC}"
cd backend
python3 app.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Check if backend is running
if curl -s http://localhost:5001/api/products > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend server is running${NC}"
else
    echo -e "${YELLOW}⚠ Backend server starting... (check backend.log for details)${NC}"
fi

# Start frontend server
echo -e "${GREEN}Starting React frontend server on http://localhost:3000...${NC}"
cd frontend
BROWSER=none npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
sleep 5

echo ""
echo -e "${GREEN}=========================================="
echo "Application Started Successfully!"
echo "==========================================${NC}"
echo ""
echo "Backend:  http://localhost:5001"
echo "Frontend: http://localhost:3000"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Logs:"
echo "  - Backend:  backend.log"
echo "  - Frontend: frontend.log"
echo ""
echo "To stop the servers:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Or run: ./stop_app.sh"
echo ""

# Save PIDs to file
echo "$BACKEND_PID $FRONTEND_PID" > .app_pids
