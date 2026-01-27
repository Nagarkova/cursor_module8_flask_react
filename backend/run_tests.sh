#!/bin/bash

# Comprehensive Test Runner Script
# Runs all test suites with coverage reporting

echo "=========================================="
echo "Running E-Commerce Checkout Test Suite"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: Virtual environment not activated"
    echo "Activating virtual environment..."
    source venv/bin/activate 2>/dev/null || echo "Please activate your virtual environment first"
fi

# Install dependencies if needed
echo -e "${BLUE}Checking dependencies...${NC}"
pip install -q -r requirements.txt

echo ""
echo -e "${BLUE}=========================================="
echo "Running Original Test Suite"
echo "==========================================${NC}"
pytest test_checkout.py -v --tb=short

echo ""
echo -e "${BLUE}=========================================="
echo "Running Expanded Test Suite"
echo "==========================================${NC}"
pytest test_checkout_expanded.py -v --tb=short

echo ""
echo -e "${BLUE}=========================================="
echo "Running All Tests with Coverage"
echo "==========================================${NC}"
pytest test_checkout.py test_checkout_expanded.py \
    --cov=app \
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
