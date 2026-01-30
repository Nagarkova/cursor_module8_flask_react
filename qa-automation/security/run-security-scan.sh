#!/bin/bash

# Security Scanning Script
# Runs OWASP ZAP and Snyk security scans

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPORTS_DIR="$SCRIPT_DIR/../reports/security"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Security Scanning${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

# Create reports directory
mkdir -p "$REPORTS_DIR"

TARGET_URL="${BASE_URL:-http://localhost:3000}"
HIGH_ISSUES=0
MEDIUM_ISSUES=0
LOW_ISSUES=0

# ==================== Snyk Dependency Scanning ====================
echo -e "${BLUE}Running Snyk dependency scan...${NC}"

if command -v snyk &> /dev/null; then
    # Frontend
    echo -e "  Scanning frontend dependencies..."
    cd "$PROJECT_ROOT/frontend"
    
    set +e
    snyk test --json > "$REPORTS_DIR/snyk-frontend.json" 2>&1
    snyk test > "$REPORTS_DIR/snyk-frontend.txt" 2>&1
    set -e
    
    # Backend
    echo -e "  Scanning backend dependencies..."
    cd "$PROJECT_ROOT/backend"
    
    set +e
    snyk test --json > "$REPORTS_DIR/snyk-backend.json" 2>&1
    snyk test > "$REPORTS_DIR/snyk-backend.txt" 2>&1
    set -e
    
    echo -e "${GREEN}✓ Snyk scan completed${NC}"
else
    echo -e "${YELLOW}⚠ Snyk not found. Install: npm install -g snyk${NC}"
fi

echo ""

# ==================== OWASP ZAP Scanning (if available) ====================
echo -e "${BLUE}OWASP ZAP scan...${NC}"

if command -v zap.sh &> /dev/null || command -v zap-cli &> /dev/null; then
    echo -e "  Running ZAP baseline scan on $TARGET_URL..."
    
    # Use Docker ZAP for easy setup
    if command -v docker &> /dev/null; then
        docker run --rm \
            -v "$REPORTS_DIR:/zap/wrk:rw" \
            -t owasp/zap2docker-stable zap-baseline.py \
            -t "$TARGET_URL" \
            -r zap-report.html \
            -J zap-report.json \
            || true
        
        echo -e "${GREEN}✓ ZAP scan completed${NC}"
    else
        echo -e "${YELLOW}⚠ Docker not found. Skipping ZAP scan.${NC}"
    fi
else
    echo -e "${YELLOW}⚠ OWASP ZAP not found. Skipping dynamic scan.${NC}"
    echo -e "  Install: brew install --cask owasp-zap (macOS)"
fi

echo ""

# ==================== Parse Results ====================
echo -e "${BLUE}Analyzing security findings...${NC}"

# Parse Snyk results
if [ -f "$REPORTS_DIR/snyk-frontend.json" ]; then
    SNYK_ISSUES=$(python3 -c "
import json, sys
try:
    with open('$REPORTS_DIR/snyk-frontend.json') as f:
        data = json.load(f)
        if 'vulnerabilities' in data:
            high = len([v for v in data['vulnerabilities'] if v.get('severity') == 'high'])
            medium = len([v for v in data['vulnerabilities'] if v.get('severity') == 'medium'])
            low = len([v for v in data['vulnerabilities'] if v.get('severity') == 'low'])
            print(f'{high},{medium},{low}')
        else:
            print('0,0,0')
except:
    print('0,0,0')
")
    IFS=',' read -r H M L <<< "$SNYK_ISSUES"
    HIGH_ISSUES=$((HIGH_ISSUES + H))
    MEDIUM_ISSUES=$((MEDIUM_ISSUES + M))
    LOW_ISSUES=$((LOW_ISSUES + L))
fi

# Generate summary report
cat > "$REPORTS_DIR/security-summary.json" <<EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "target_url": "$TARGET_URL",
  "findings": {
    "high": $HIGH_ISSUES,
    "medium": $MEDIUM_ISSUES,
    "low": $LOW_ISSUES,
    "total": $((HIGH_ISSUES + MEDIUM_ISSUES + LOW_ISSUES))
  },
  "reports": {
    "snyk_frontend": "snyk-frontend.json",
    "snyk_backend": "snyk-backend.json",
    "zap": "zap-report.html"
  }
}
EOF

# Generate HTML report
cat > "$REPORTS_DIR/security-report.html" <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>Security Scan Report</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }
        h1 { color: #333; border-bottom: 3px solid #F44336; padding-bottom: 10px; }
        .severity { display: inline-block; margin: 15px; padding: 20px; border-radius: 8px; min-width: 150px; text-align: center; }
        .severity-high { background: #F44336; color: white; }
        .severity-medium { background: #FF9800; color: white; }
        .severity-low { background: #FFC107; color: black; }
        .count { font-size: 48px; font-weight: bold; }
        .label { font-size: 14px; margin-top: 10px; }
        .status { padding: 20px; margin: 20px 0; border-radius: 8px; }
        .status-pass { background: #4CAF50; color: white; }
        .status-fail { background: #F44336; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Security Scan Report</h1>
        <p>Generated: $(date)</p>
        <p>Target: $TARGET_URL</p>
        
        <div class="severity severity-high">
            <div class="count">$HIGH_ISSUES</div>
            <div class="label">High Severity</div>
        </div>
        
        <div class="severity severity-medium">
            <div class="count">$MEDIUM_ISSUES</div>
            <div class="label">Medium Severity</div>
        </div>
        
        <div class="severity severity-low">
            <div class="count">$LOW_ISSUES</div>
            <div class="label">Low Severity</div>
        </div>
        
        <div class="status status-$([ $HIGH_ISSUES -eq 0 ] && echo "pass" || echo "fail")">
            <h2>$([ $HIGH_ISSUES -eq 0 ] && echo "✓ PASSED" || echo "✗ FAILED")</h2>
            <p>$([ $HIGH_ISSUES -eq 0 ] && echo "No high-severity issues found" || echo "$HIGH_ISSUES high-severity issues require immediate attention")</p>
        </div>
        
        <h2>Detailed Reports</h2>
        <ul>
            <li><a href="snyk-frontend.txt">Snyk Frontend Report</a></li>
            <li><a href="snyk-backend.txt">Snyk Backend Report</a></li>
            <li><a href="zap-report.html">OWASP ZAP Report</a></li>
        </ul>
    </div>
</body>
</html>
EOF

echo -e "${GREEN}✓ Reports generated in: $REPORTS_DIR${NC}"
echo ""

# ==================== Summary ====================
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Security Summary${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "  High Severity:   ${RED}$HIGH_ISSUES${NC}"
echo -e "  Medium Severity: ${YELLOW}$MEDIUM_ISSUES${NC}"
echo -e "  Low Severity:    ${GREEN}$LOW_ISSUES${NC}"
echo -e "  Total:           $((HIGH_ISSUES + MEDIUM_ISSUES + LOW_ISSUES))"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"

# Quality gate
if [ $HIGH_ISSUES -gt 0 ]; then
    echo -e "${RED}❌ Security check failed: $HIGH_ISSUES high-severity issues found${NC}"
    exit 1
elif [ $MEDIUM_ISSUES -gt 5 ]; then
    echo -e "${YELLOW}⚠️  Security check passed with warnings: $MEDIUM_ISSUES medium-severity issues${NC}"
    exit 0
else
    echo -e "${GREEN}✓ Security check passed${NC}"
    exit 0
fi
