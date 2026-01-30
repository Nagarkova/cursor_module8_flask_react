#!/bin/bash

# Backend Startup Script
echo "=========================================="
echo "Starting Flask Backend Server"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${BLUE}Installing/updating dependencies...${NC}"
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1

# Initialize database
echo -e "${BLUE}Initializing database...${NC}"
python3 -c "from app import app, db, init_db; app.app_context().push(); init_db(); print('Database initialized')" 2>/dev/null || echo "Database already initialized"

# Start Flask server
echo ""
echo -e "${GREEN}=========================================="
echo "Backend Server Starting"
echo "==========================================${NC}"
echo ""
echo "Backend URL: http://localhost:5001"
echo "API Endpoints:"
echo "  - GET  http://localhost:5001/api/products"
echo "  - POST http://localhost:5001/api/cart/add"
echo "  - GET  http://localhost:5001/api/cart?session_id=<id>"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

python3 app.py
