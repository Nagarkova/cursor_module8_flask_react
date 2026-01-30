#!/bin/bash

# Performance Testing Script using k6
# Tests load, stress, and spike scenarios

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPORTS_DIR="$SCRIPT_DIR/../reports/performance"
SCENARIOS_DIR="$SCRIPT_DIR/scenarios"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Performance Testing with k6${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

# Create reports directory
mkdir -p "$REPORTS_DIR"

# Check if k6 is installed
if ! command -v k6 &> /dev/null; then
    echo -e "${YELLOW}k6 is not installed. Installing...${NC}"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install k6
    else
        echo -e "${YELLOW}Please install k6: https://k6.io/docs/getting-started/installation/${NC}"
        exit 1
    fi
fi

# Set environment variables
export BASE_URL="${BASE_URL:-http://localhost:3000}"
export API_URL="${API_URL:-http://localhost:5001}"

echo -e "${GREEN}Target URLs:${NC}"
echo -e "  Frontend: $BASE_URL"
echo -e "  API: $API_URL"
echo ""

# Test scenarios
SCENARIOS=("load-test" "stress-test")

for SCENARIO in "${SCENARIOS[@]}"; do
    echo -e "${BLUE}Running $SCENARIO...${NC}"
    
    k6 run \
        --out json="$REPORTS_DIR/${SCENARIO}-results.json" \
        --summary-export="$REPORTS_DIR/${SCENARIO}-summary.json" \
        "$SCENARIOS_DIR/${SCENARIO}.js"
    
    echo -e "${GREEN}✓ $SCENARIO completed${NC}"
    echo ""
done

# Generate HTML report
python3 - <<EOF
import json
import os
from datetime import datetime

reports_dir = "$REPORTS_DIR"
scenarios = ["load-test", "stress-test"]

html = '''<!DOCTYPE html>
<html>
<head>
    <title>Performance Test Report</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }
        h1 { color: #333; border-bottom: 3px solid #2196F3; padding-bottom: 10px; }
        .metric-card { display: inline-block; margin: 15px; padding: 20px; border-radius: 8px; background: #f9f9f9; min-width: 200px; }
        .metric-value { font-size: 36px; font-weight: bold; color: #2196F3; }
        .metric-label { font-size: 14px; color: #666; margin-top: 5px; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #2196F3; color: white; }
        .pass { color: #4CAF50; font-weight: bold; }
        .fail { color: #F44336; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Performance Test Report</h1>
        <p>Generated: ''' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '''</p>
'''

for scenario in scenarios:
    summary_file = os.path.join(reports_dir, f"{scenario}-summary.json")
    if os.path.exists(summary_file):
        with open(summary_file) as f:
            data = json.load(f)
            
        metrics = data.get('metrics', {})
        
        html += f'''
        <h2>{scenario.replace("-", " ").title()}</h2>
        <div class="metric-card">
            <div class="metric-value">{metrics.get('http_reqs', {}).get('count', 'N/A')}</div>
            <div class="metric-label">Total Requests</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{metrics.get('http_req_duration', {}).get('avg', 'N/A'):.0f}ms</div>
            <div class="metric-label">Avg Response Time</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{metrics.get('http_req_duration', {}).get('p(95)', 'N/A'):.0f}ms</div>
            <div class="metric-label">P95 Response Time</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{metrics.get('http_req_failed', {}).get('rate', 0)*100:.2f}%</div>
            <div class="metric-label">Error Rate</div>
        </div>
        '''

html += '''
    </div>
</body>
</html>
'''

with open(os.path.join(reports_dir, "performance-report.html"), "w") as f:
    f.write(html)

print("HTML report generated successfully")
EOF

echo -e "${GREEN}✓ Performance testing completed${NC}"
echo -e "${GREEN}✓ View report: $REPORTS_DIR/performance-report.html${NC}"
