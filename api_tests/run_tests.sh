#!/bin/bash

# Comprehensive API Test Runner Script
# Runs all API tests with coverage reporting

echo "=========================================="
echo "Running REST API Test Suite"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${YELLOW}⚠️  Warning: Virtual environment not activated${NC}"
    echo "Activating virtual environment..."
    source venv/bin/activate 2>/dev/null || echo "Please activate your virtual environment first"
fi

# Install dependencies if needed
echo -e "${BLUE}Checking dependencies...${NC}"
pip install -q -r requirements.txt

echo ""
echo -e "${BLUE}=========================================="
echo "Running User Management Tests"
echo "==========================================${NC}"
pytest test_user_management.py -v --tb=short

echo ""
echo -e "${BLUE}=========================================="
echo "Running Product Catalog Tests"
echo "==========================================${NC}"
pytest test_product_catalog.py -v --tb=short

echo ""
echo -e "${BLUE}=========================================="
echo "Running Orders Tests"
echo "==========================================${NC}"
pytest test_orders.py -v --tb=short

echo ""
echo -e "${BLUE}=========================================="
echo "Running Rate Limiting Tests"
echo "==========================================${NC}"
pytest test_rate_limiting.py -v --tb=short

echo ""
echo -e "${BLUE}=========================================="
echo "Running Error Response Tests"
echo "==========================================${NC}"
pytest test_error_responses.py -v --tb=short

echo ""
echo -e "${BLUE}=========================================="
echo "Running All Tests with Coverage"
echo "==========================================${NC}"
pytest . \
    --cov=. \
    --cov-report=term-missing \
    --cov-report=html \
    -v

echo ""
echo -e "${GREEN}=========================================="
echo "Test Summary"
echo "==========================================${NC}"
echo "Coverage report generated in htmlcov/index.html"
echo ""
echo "To view coverage report:"
echo "  open htmlcov/index.html"
echo ""
