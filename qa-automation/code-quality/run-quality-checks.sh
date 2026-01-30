#!/bin/bash

# Code Quality Check Script
# Runs ESLint and Pylint with comprehensive reporting

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPORTS_DIR="$SCRIPT_DIR/../reports/code-quality"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Code Quality Analysis${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

# Create reports directory
mkdir -p "$REPORTS_DIR"

# Initialize results
ESLINT_SCORE=0
PYLINT_SCORE=0
TOTAL_ISSUES=0

# ==================== Frontend - ESLint ====================
echo -e "${BLUE}Running ESLint on Frontend...${NC}"

cd "$PROJECT_ROOT/frontend"

if [ -f "package.json" ]; then
    # Install eslint if not present
    if ! command -v eslint &> /dev/null; then
        npm install --save-dev eslint
    fi

    # Run ESLint
    set +e
    eslint src/ \
        --config "$SCRIPT_DIR/.eslintrc.json" \
        --format json \
        --output-file "$REPORTS_DIR/eslint-report.json" \
        2>&1
    
    eslint src/ \
        --config "$SCRIPT_DIR/.eslintrc.json" \
        --format html \
        --output-file "$REPORTS_DIR/eslint-report.html" \
        2>&1
    
    ESLINT_EXIT_CODE=$?
    set -e

    # Parse results
    if [ -f "$REPORTS_DIR/eslint-report.json" ]; then
        ESLINT_ERRORS=$(cat "$REPORTS_DIR/eslint-report.json" | python3 -c "
import sys, json
data = json.load(sys.stdin)
errors = sum(f.get('errorCount', 0) for f in data)
warnings = sum(f.get('warningCount', 0) for f in data)
print(f'{errors},{warnings}')
")
        IFS=',' read -r ERRORS WARNINGS <<< "$ESLINT_ERRORS"
        
        echo -e "${YELLOW}  Errors: $ERRORS${NC}"
        echo -e "${YELLOW}  Warnings: $WARNINGS${NC}"
        
        TOTAL_ISSUES=$((TOTAL_ISSUES + ERRORS + WARNINGS))
        
        # Calculate score (10 = perfect, 0 = worst)
        if [ "$ERRORS" -eq 0 ] && [ "$WARNINGS" -eq 0 ]; then
            ESLINT_SCORE=10
        elif [ "$ERRORS" -eq 0 ]; then
            ESLINT_SCORE=$(python3 -c "print(max(0, 10 - ($WARNINGS * 0.1)))")
        else
            ESLINT_SCORE=$(python3 -c "print(max(0, 10 - ($ERRORS * 0.5) - ($WARNINGS * 0.1)))")
        fi
        
        echo -e "${GREEN}  ESLint Score: $ESLINT_SCORE/10${NC}"
    fi
else
    echo -e "${YELLOW}  Skipped: package.json not found${NC}"
fi

echo ""

# ==================== Backend - Pylint ====================
echo -e "${BLUE}Running Pylint on Backend...${NC}"

cd "$PROJECT_ROOT/backend"

if [ -f "app.py" ]; then
    # Install pylint if not present
    if ! command -v pylint &> /dev/null; then
        pip install pylint
    fi

    # Run Pylint
    set +e
    pylint *.py \
        --rcfile="$SCRIPT_DIR/.pylintrc" \
        --output-format=json \
        > "$REPORTS_DIR/pylint-report.json" \
        2>&1
    
    PYLINT_EXIT_CODE=$?
    
    # Generate HTML report
    pylint *.py \
        --rcfile="$SCRIPT_DIR/.pylintrc" \
        --output-format=text \
        > "$REPORTS_DIR/pylint-report.txt" \
        2>&1
    
    set -e

    # Parse results
    if [ -f "$REPORTS_DIR/pylint-report.json" ]; then
        PYLINT_STATS=$(cat "$REPORTS_DIR/pylint-report.json" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if isinstance(data, list):
        errors = len([m for m in data if m.get('type') == 'error'])
        warnings = len([m for m in data if m.get('type') == 'warning'])
        print(f'{errors},{warnings}')
    else:
        print('0,0')
except:
    print('0,0')
")
        IFS=',' read -r ERRORS WARNINGS <<< "$PYLINT_STATS"
        
        echo -e "${YELLOW}  Errors: $ERRORS${NC}"
        echo -e "${YELLOW}  Warnings: $WARNINGS${NC}"
        
        TOTAL_ISSUES=$((TOTAL_ISSUES + ERRORS + WARNINGS))
        
        # Calculate score
        if [ "$ERRORS" -eq 0 ] && [ "$WARNINGS" -eq 0 ]; then
            PYLINT_SCORE=10
        elif [ "$ERRORS" -eq 0 ]; then
            PYLINT_SCORE=$(python3 -c "print(max(0, 10 - ($WARNINGS * 0.1)))")
        else
            PYLINT_SCORE=$(python3 -c "print(max(0, 10 - ($ERRORS * 0.5) - ($WARNINGS * 0.1)))")
        fi
        
        echo -e "${GREEN}  Pylint Score: $PYLINT_SCORE/10${NC}"
    fi
else
    echo -e "${YELLOW}  Skipped: app.py not found${NC}"
fi

echo ""

# ==================== Generate Summary ====================
echo -e "${BLUE}Generating Quality Summary...${NC}"

OVERALL_SCORE=$(python3 -c "print(round(($ESLINT_SCORE + $PYLINT_SCORE) / 2, 2))")

cat > "$REPORTS_DIR/quality-summary.json" <<EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "overall_score": $OVERALL_SCORE,
  "eslint_score": $ESLINT_SCORE,
  "pylint_score": $PYLINT_SCORE,
  "total_issues": $TOTAL_ISSUES,
  "reports": {
    "eslint_json": "eslint-report.json",
    "eslint_html": "eslint-report.html",
    "pylint_json": "pylint-report.json",
    "pylint_text": "pylint-report.txt"
  }
}
EOF

# Generate HTML summary
cat > "$REPORTS_DIR/quality-report.html" <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>Code Quality Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }
        .score-card { display: inline-block; margin: 20px; padding: 20px; border-radius: 8px; text-align: center; min-width: 150px; }
        .score-excellent { background: #4CAF50; color: white; }
        .score-good { background: #8BC34A; color: white; }
        .score-warning { background: #FFC107; color: black; }
        .score-poor { background: #F44336; color: white; }
        .score-number { font-size: 48px; font-weight: bold; }
        .score-label { font-size: 14px; margin-top: 10px; }
        .report-links { margin-top: 30px; }
        .report-link { display: inline-block; margin: 10px; padding: 10px 20px; background: #2196F3; color: white; text-decoration: none; border-radius: 4px; }
        .report-link:hover { background: #1976D2; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Code Quality Report</h1>
        <p>Generated: $(date)</p>
        
        <div class="score-card score-$([ $(echo "$OVERALL_SCORE >= 8" | bc) -eq 1 ] && echo "excellent" || [ $(echo "$OVERALL_SCORE >= 6" | bc) -eq 1 ] && echo "good" || [ $(echo "$OVERALL_SCORE >= 4" | bc) -eq 1 ] && echo "warning" || echo "poor")">
            <div class="score-number">$OVERALL_SCORE</div>
            <div class="score-label">Overall Score</div>
        </div>
        
        <div class="score-card score-$([ $(echo "$ESLINT_SCORE >= 8" | bc) -eq 1 ] && echo "excellent" || [ $(echo "$ESLINT_SCORE >= 6" | bc) -eq 1 ] && echo "good" || [ $(echo "$ESLINT_SCORE >= 4" | bc) -eq 1 ] && echo "warning" || echo "poor")">
            <div class="score-number">$ESLINT_SCORE</div>
            <div class="score-label">ESLint Score</div>
        </div>
        
        <div class="score-card score-$([ $(echo "$PYLINT_SCORE >= 8" | bc) -eq 1 ] && echo "excellent" || [ $(echo "$PYLINT_SCORE >= 6" | bc) -eq 1 ] && echo "good" || [ $(echo "$PYLINT_SCORE >= 4" | bc) -eq 1 ] && echo "warning" || echo "poor")">
            <div class="score-number">$PYLINT_SCORE</div>
            <div class="score-label">Pylint Score</div>
        </div>
        
        <h2>Summary</h2>
        <p>Total Issues Found: <strong>$TOTAL_ISSUES</strong></p>
        
        <div class="report-links">
            <h3>Detailed Reports</h3>
            <a href="eslint-report.html" class="report-link">ESLint Report</a>
            <a href="pylint-report.txt" class="report-link">Pylint Report</a>
        </div>
    </div>
</body>
</html>
EOF

echo -e "${GREEN}✓ Reports generated in: $REPORTS_DIR${NC}"
echo -e "${GREEN}✓ View HTML report: $REPORTS_DIR/quality-report.html${NC}"
echo ""

# ==================== Final Summary ====================
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Quality Summary${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "  Overall Score:  ${GREEN}$OVERALL_SCORE/10${NC}"
echo -e "  ESLint Score:   ${GREEN}$ESLINT_SCORE/10${NC}"
echo -e "  Pylint Score:   ${GREEN}$PYLINT_SCORE/10${NC}"
echo -e "  Total Issues:   ${YELLOW}$TOTAL_ISSUES${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"

# Exit with appropriate code
if [ $(echo "$OVERALL_SCORE < 6" | bc) -eq 1 ]; then
    echo -e "${RED}❌ Quality check failed (score < 6.0)${NC}"
    exit 1
elif [ $(echo "$OVERALL_SCORE < 8" | bc) -eq 1 ]; then
    echo -e "${YELLOW}⚠️  Quality check passed with warnings (score < 8.0)${NC}"
    exit 0
else
    echo -e "${GREEN}✓ Quality check passed${NC}"
    exit 0
fi
