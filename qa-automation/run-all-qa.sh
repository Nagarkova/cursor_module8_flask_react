#!/bin/bash

# Master QA Automation Script
# Runs all quality assurance checks: E2E tests, code quality, security, and performance

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPORTS_DIR="$SCRIPT_DIR/reports"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Parse arguments
SKIP_PERFORMANCE=false
SKIP_SECURITY=false
QUICK_MODE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-performance)
            SKIP_PERFORMANCE=true
            shift
            ;;
        --skip-security)
            SKIP_SECURITY=true
            shift
            ;;
        --quick)
            QUICK_MODE=true
            SKIP_PERFORMANCE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--skip-performance] [--skip-security] [--quick]"
            exit 1
            ;;
    esac
done

# Banner
clear
echo -e "${CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     ██████╗  █████╗      █████╗ ██╗   ██╗████████╗ ██████╗  ║
║    ██╔═══██╗██╔══██╗    ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗ ║
║    ██║   ██║███████║    ███████║██║   ██║   ██║   ██║   ██║ ║
║    ██║▄▄ ██║██╔══██║    ██╔══██║██║   ██║   ██║   ██║   ██║ ║
║    ╚██████╔╝██║  ██║    ██║  ██║╚██████╔╝   ██║   ╚██████╔╝ ║
║     ╚══▀▀═╝ ╚═╝  ╚═╝    ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝  ║
║                                                               ║
║              Quality Assurance Automation Suite              ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${BLUE}Starting comprehensive QA checks...${NC}"
echo -e "${BLUE}Timestamp: $(date)${NC}"
echo ""

# Create reports directory
mkdir -p "$REPORTS_DIR"

# Track results
ALL_TESTS_PASSED=true
SUMMARY_FILE="$REPORTS_DIR/qa-summary.json"

# Initialize summary
cat > "$SUMMARY_FILE" <<EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "results": {}
}
EOF

# ==================== 1. E2E Tests ====================
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  [1/5] Running E2E Tests${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

cd "$SCRIPT_DIR/e2e-tests"

if [ -f "package.json" ]; then
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo "Installing dependencies..."
        npm install
    fi
    
    set +e
    npm test
    E2E_EXIT=$?
    set -e
    
    if [ $E2E_EXIT -eq 0 ]; then
        echo -e "${GREEN}✓ E2E tests passed${NC}"
    else
        echo -e "${RED}✗ E2E tests failed${NC}"
        ALL_TESTS_PASSED=false
    fi
else
    echo -e "${YELLOW}⚠ E2E tests not found, skipping${NC}"
fi

echo ""

# ==================== 2. Code Quality ====================
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  [2/5] Running Code Quality Checks${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

set +e
bash "$SCRIPT_DIR/code-quality/run-quality-checks.sh"
QUALITY_EXIT=$?
set -e

if [ $QUALITY_EXIT -eq 0 ]; then
    echo -e "${GREEN}✓ Code quality checks passed${NC}"
else
    echo -e "${RED}✗ Code quality checks failed${NC}"
    ALL_TESTS_PASSED=false
fi

echo ""

# ==================== 3. Security Scanning ====================
if [ "$SKIP_SECURITY" = false ]; then
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  [3/5] Running Security Scans${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo ""
    
    set +e
    bash "$SCRIPT_DIR/security/run-security-scan.sh"
    SECURITY_EXIT=$?
    set -e
    
    if [ $SECURITY_EXIT -eq 0 ]; then
        echo -e "${GREEN}✓ Security scans passed${NC}"
    else
        echo -e "${RED}✗ Security scans failed${NC}"
        ALL_TESTS_PASSED=false
    fi
else
    echo -e "${YELLOW}⚠ Security scans skipped${NC}"
    SECURITY_EXIT=0
fi

echo ""

# ==================== 4. Performance Tests ====================
if [ "$SKIP_PERFORMANCE" = false ]; then
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  [4/5] Running Performance Tests${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo ""
    
    set +e
    bash "$SCRIPT_DIR/performance/run-performance-tests.sh"
    PERF_EXIT=$?
    set -e
    
    if [ $PERF_EXIT -eq 0 ]; then
        echo -e "${GREEN}✓ Performance tests passed${NC}"
    else
        echo -e "${RED}✗ Performance tests failed${NC}"
        ALL_TESTS_PASSED=false
    fi
else
    echo -e "${YELLOW}⚠ Performance tests skipped${NC}"
    PERF_EXIT=0
fi

echo ""

# ==================== 5. Generate Dashboard ====================
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  [5/5] Generating Quality Dashboard${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

# Generate comprehensive dashboard
python3 - <<'PYTHON_SCRIPT'
import json
import os
from datetime import datetime
from pathlib import Path

reports_dir = os.environ.get('REPORTS_DIR', 'reports')
dashboard_file = os.path.join(reports_dir, 'dashboard.html')

# Collect all metrics
metrics = {
    'e2e_tests': {'passed': True, 'total': 0, 'failed': 0},
    'code_quality': {'score': 0},
    'security': {'high': 0, 'medium': 0, 'low': 0},
    'performance': {'p95': 0, 'error_rate': 0}
}

# Read E2E results
try:
    with open(os.path.join(reports_dir, 'test-results/results.json')) as f:
        e2e_data = json.load(f)
        # Parse Playwright results
except:
    pass

# Read quality results
try:
    with open(os.path.join(reports_dir, 'code-quality/quality-summary.json')) as f:
        quality_data = json.load(f)
        metrics['code_quality']['score'] = quality_data.get('overall_score', 0)
except:
    pass

# Read security results
try:
    with open(os.path.join(reports_dir, 'security/security-summary.json')) as f:
        security_data = json.load(f)
        findings = security_data.get('findings', {})
        metrics['security'] = findings
except:
    pass

# Generate HTML dashboard
html = f'''<!DOCTYPE html>
<html>
<head>
    <title>QA Dashboard</title>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .dashboard {{ 
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{ font-size: 36px; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; }}
        .content {{ padding: 40px; }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .metric-card {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 25px;
            border-left: 4px solid #667eea;
            transition: transform 0.2s;
        }}
        .metric-card:hover {{ transform: translateY(-5px); }}
        .metric-value {{
            font-size: 48px;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }}
        .metric-label {{
            color: #6c757d;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .status-badge {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            margin-top: 10px;
        }}
        .status-pass {{ background: #d4edda; color: #155724; }}
        .status-fail {{ background: #f8d7da; color: #721c24; }}
        .status-warn {{ background: #fff3cd; color: #856404; }}
        .report-links {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 30px;
        }}
        .report-link {{
            display: block;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            text-align: center;
            transition: transform 0.2s;
        }}
        .report-link:hover {{ transform: scale(1.05); }}
        .chart {{ 
            background: #f8f9fa;
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>QA Dashboard</h1>
            <p>Quality Assurance Metrics & Reports</p>
            <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        
        <div class="content">
            <h2>Key Metrics</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">Code Quality Score</div>
                    <div class="metric-value">{metrics['code_quality']['score']:.1f}/10</div>
                    <span class="status-badge status-{'pass' if metrics['code_quality']['score'] >= 8 else 'warn' if metrics['code_quality']['score'] >= 6 else 'fail'}">
                        {'Excellent' if metrics['code_quality']['score'] >= 8 else 'Good' if metrics['code_quality']['score'] >= 6 else 'Needs Improvement'}
                    </span>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">Security Issues</div>
                    <div class="metric-value">{metrics['security'].get('high', 0)}</div>
                    <span class="status-badge status-{'pass' if metrics['security'].get('high', 0) == 0 else 'fail'}">
                        {'No Critical Issues' if metrics['security'].get('high', 0) == 0 else 'Action Required'}
                    </span>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">E2E Tests</div>
                    <div class="metric-value">{'✓' if metrics['e2e_tests']['passed'] else '✗'}</div>
                    <span class="status-badge status-{'pass' if metrics['e2e_tests']['passed'] else 'fail'}">
                        {'All Passed' if metrics['e2e_tests']['passed'] else 'Some Failed'}
                    </span>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">Performance</div>
                    <div class="metric-value">{metrics['performance']['p95']:.0f}ms</div>
                    <span class="status-badge status-{'pass' if metrics['performance']['p95'] < 2000 else 'warn'}">
                        {'Optimal' if metrics['performance']['p95'] < 2000 else 'Review Needed'}
                    </span>
                </div>
            </div>
            
            <h2>Detailed Reports</h2>
            <div class="report-links">
                <a href="test-results/playwright-report/index.html" class="report-link">E2E Test Results</a>
                <a href="code-quality/quality-report.html" class="report-link">Code Quality Report</a>
                <a href="security/security-report.html" class="report-link">Security Scan Report</a>
                <a href="performance/performance-report.html" class="report-link">Performance Report</a>
            </div>
        </div>
    </div>
</body>
</html>'''

with open(dashboard_file, 'w') as f:
    f.write(html)

print(f"Dashboard generated: {dashboard_file}")
PYTHON_SCRIPT

echo -e "${GREEN}✓ Dashboard generated${NC}"
echo ""

# ==================== Final Summary ====================
echo -e "${CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                      QA SUMMARY                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

if [ "$ALL_TESTS_PASSED" = true ]; then
    echo -e "${GREEN}✓ All QA checks passed successfully!${NC}"
    echo -e "${GREEN}✓ View dashboard: $REPORTS_DIR/dashboard.html${NC}"
    exit 0
else
    echo -e "${RED}✗ Some QA checks failed. Please review the reports.${NC}"
    echo -e "${YELLOW}  Dashboard: $REPORTS_DIR/dashboard.html${NC}"
    exit 1
fi
