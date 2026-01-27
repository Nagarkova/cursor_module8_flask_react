#!/bin/bash

# Frontend Test Runner Script
# Runs Jest tests with coverage

echo "=========================================="
echo "Running Frontend Test Suite"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

echo -e "${BLUE}Running Jest tests...${NC}"
npm test -- --coverage --watchAll=false

echo ""
echo -e "${GREEN}=========================================="
echo "Test Complete"
echo "==========================================${NC}"
echo "Coverage report available in coverage/ directory"
echo ""
