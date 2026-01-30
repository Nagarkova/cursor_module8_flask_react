#!/bin/bash

# Frontend Startup Script
echo "=========================================="
echo "Starting React Frontend Server"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    npm install
fi

# Start React development server
echo ""
echo -e "${GREEN}=========================================="
echo "Frontend Server Starting"
echo "==========================================${NC}"
echo ""
echo "Frontend URL: http://localhost:3000"
echo "Backend API: http://localhost:5001"
echo ""
echo "The browser will open automatically"
echo "Press CTRL+C to stop the server"
echo ""

BROWSER=none npm start
