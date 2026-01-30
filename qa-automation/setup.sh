#!/bin/bash

# QA Automation Setup Script
# Installs all dependencies and prepares the environment

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  QA Automation Setup${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

# ==================== Install Node.js Dependencies ====================
echo -e "${BLUE}Installing E2E test dependencies...${NC}"
cd "$SCRIPT_DIR/e2e-tests"

if [ -f "package.json" ]; then
    npm install
    npx playwright install
    echo -e "${GREEN}✓ E2E dependencies installed${NC}"
fi

echo ""

# ==================== Install Python Tools ====================
echo -e "${BLUE}Installing Python tools...${NC}"

pip install --upgrade pip
pip install pylint bandit safety

echo -e "${GREEN}✓ Python tools installed${NC}"
echo ""

# ==================== Install k6 ====================
echo -e "${BLUE}Checking k6 installation...${NC}"

if ! command -v k6 &> /dev/null; then
    echo -e "${YELLOW}k6 not found. Installing...${NC}"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install k6
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo gpg -k
        sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
        echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
        sudo apt-get update
        sudo apt-get install k6
    fi
    
    echo -e "${GREEN}✓ k6 installed${NC}"
else
    echo -e "${GREEN}✓ k6 already installed${NC}"
fi

echo ""

# ==================== Install Snyk (Optional) ====================
echo -e "${BLUE}Checking Snyk installation...${NC}"

if ! command -v snyk &> /dev/null; then
    echo -e "${YELLOW}Snyk not found. Installing...${NC}"
    npm install -g snyk
    echo -e "${GREEN}✓ Snyk installed${NC}"
    echo -e "${YELLOW}  Remember to authenticate: snyk auth${NC}"
else
    echo -e "${GREEN}✓ Snyk already installed${NC}"
fi

echo ""

# ==================== Create Report Directories ====================
echo -e "${BLUE}Creating report directories...${NC}"

mkdir -p "$SCRIPT_DIR/reports/test-results"
mkdir -p "$SCRIPT_DIR/reports/code-quality"
mkdir -p "$SCRIPT_DIR/reports/security"
mkdir -p "$SCRIPT_DIR/reports/performance"
mkdir -p "$SCRIPT_DIR/reports/screenshots"

echo -e "${GREEN}✓ Report directories created${NC}"
echo ""

# ==================== Make Scripts Executable ====================
echo -e "${BLUE}Making scripts executable...${NC}"

chmod +x "$SCRIPT_DIR/run-all-qa.sh"
chmod +x "$SCRIPT_DIR/code-quality/run-quality-checks.sh"
chmod +x "$SCRIPT_DIR/security/run-security-scan.sh"
chmod +x "$SCRIPT_DIR/performance/run-performance-tests.sh"

echo -e "${GREEN}✓ Scripts are now executable${NC}"
echo ""

# ==================== Success ====================
echo -e "${GREEN}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                   ║${NC}"
echo -e "${GREEN}║      ✓ Setup completed successfully!              ║${NC}"
echo -e "${GREEN}║                                                   ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo -e "  1. Configure environment variables in .env"
echo -e "  2. Run: ./qa-automation/run-all-qa.sh"
echo -e "  3. View dashboard: qa-automation/reports/dashboard.html"
echo ""
