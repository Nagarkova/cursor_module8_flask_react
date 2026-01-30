# QA Automation System

## Overview

This directory contains a complete Quality Assurance automation system including:
- E2E Test Automation (Playwright + Page Object Model)
- Code Quality Checks (ESLint, Pylint)
- Security Scanning (OWASP ZAP, Snyk)
- Performance Testing (k6)
- Quality Dashboard
- Automated Report Generation

## Quick Start

```bash
# Install all dependencies
./qa-automation/setup.sh

# Run all QA checks
./qa-automation/run-all-qa.sh

# View dashboard
open qa-automation/reports/dashboard.html
```

## Directory Structure

```
qa-automation/
├── e2e-tests/              # End-to-end tests with Page Object Model
│   ├── pages/              # Page Object Model classes
│   ├── tests/              # Test specifications
│   └── playwright.config.js
├── code-quality/           # Code quality configurations
│   ├── .eslintrc.json
│   ├── .pylintrc
│   └── run-quality-checks.sh
├── security/               # Security scanning
│   ├── zap/                # OWASP ZAP configuration
│   ├── snyk/               # Snyk configuration
│   └── run-security-scan.sh
├── performance/            # Performance testing
│   ├── scenarios/          # k6 test scenarios
│   └── run-performance-tests.sh
├── dashboard/              # Quality metrics dashboard
│   ├── templates/          # Dashboard HTML templates
│   ├── generate-dashboard.py
│   └── metrics-collector.py
├── reports/                # Generated reports
│   ├── test-results/
│   ├── security/
│   ├── performance/
│   └── dashboard.html
├── scripts/                # Utility scripts
│   ├── setup.sh
│   └── cleanup.sh
├── run-all-qa.sh           # Master script to run everything
└── README.md               # This file
```

## Components

### 1. E2E Test Automation
- **Framework**: Playwright with TypeScript
- **Pattern**: Page Object Model
- **Features**: Cross-browser testing, screenshots, videos
- **Reports**: HTML, JSON, JUnit XML

### 2. Code Quality
- **Frontend**: ESLint with React best practices
- **Backend**: Pylint with PEP8 standards
- **Reports**: JSON, HTML with detailed metrics

### 3. Security Scanning
- **OWASP ZAP**: Dynamic application security testing
- **Snyk**: Dependency vulnerability scanning
- **Reports**: JSON, HTML with CVE details

### 4. Performance Testing
- **Tool**: k6 by Grafana Labs
- **Scenarios**: Load, stress, spike, soak tests
- **Metrics**: Response times, throughput, error rates
- **Reports**: JSON, HTML with charts

### 5. Quality Dashboard
- **Technology**: Python + HTML/CSS/JavaScript
- **Features**: 
  - Real-time metrics visualization
  - Trend analysis
  - Quality gates
  - Executive summary
- **Updates**: Automatically after each run

## Usage

### Run Individual Components

```bash
# E2E Tests
cd qa-automation/e2e-tests
npm test

# Code Quality
./qa-automation/code-quality/run-quality-checks.sh

# Security Scan
./qa-automation/security/run-security-scan.sh

# Performance Tests
./qa-automation/performance/run-performance-tests.sh

# Generate Dashboard
python qa-automation/dashboard/generate-dashboard.py
```

### Run All QA Checks

```bash
# Complete QA suite
./qa-automation/run-all-qa.sh

# With specific options
./qa-automation/run-all-qa.sh --skip-performance  # Skip slow tests
./qa-automation/run-all-qa.sh --quick            # Quick checks only
./qa-automation/run-all-qa.sh --full             # Full comprehensive scan
```

## Quality Gates

The system enforces the following quality gates:

| Metric | Threshold | Action |
|--------|-----------|--------|
| Test Pass Rate | ≥ 95% | Fail if below |
| Code Coverage | ≥ 80% | Warn if below |
| Security Issues (High) | 0 | Fail if any |
| Security Issues (Medium) | ≤ 5 | Warn if above |
| Performance (P95) | ≤ 2s | Warn if above |
| Code Quality Score | ≥ 8.0/10 | Warn if below |

## CI/CD Integration

### GitHub Actions

```yaml
- name: Run QA Suite
  run: |
    ./qa-automation/setup.sh
    ./qa-automation/run-all-qa.sh
    
- name: Upload Reports
  uses: actions/upload-artifact@v4
  with:
    name: qa-reports
    path: qa-automation/reports/
```

### Pre-commit Hook

```bash
# Install pre-commit hook
./qa-automation/scripts/install-hooks.sh

# Runs quick checks before commit:
# - ESLint
# - Pylint
# - Unit tests
```

## Reports

All reports are generated in `qa-automation/reports/`:

- **Dashboard**: `dashboard.html` - Executive summary with all metrics
- **E2E Tests**: `test-results/playwright-report/index.html`
- **Code Quality**: `code-quality/quality-report.html`
- **Security**: `security/security-report.html`
- **Performance**: `performance/performance-report.html`

## Configuration

### Environment Variables

```bash
# Security scanning
export ZAP_API_KEY="your-zap-api-key"
export SNYK_TOKEN="your-snyk-token"

# Target URLs
export BASE_URL="http://localhost:3000"
export API_URL="http://localhost:5001"

# Performance testing
export VIRTUAL_USERS=10
export TEST_DURATION=30s
```

### Custom Thresholds

Edit `qa-automation/config.json`:

```json
{
  "quality_gates": {
    "test_pass_rate": 0.95,
    "code_coverage": 0.80,
    "security_high": 0,
    "security_medium": 5,
    "performance_p95": 2000
  }
}
```

## Troubleshooting

### Common Issues

**Tests failing to connect**
```bash
# Ensure services are running
./start_app.sh
```

**OWASP ZAP not starting**
```bash
# Install ZAP
brew install --cask owasp-zap  # macOS
# or download from https://www.zaproxy.org/download/
```

**k6 not found**
```bash
# Install k6
brew install k6  # macOS
# or see https://k6.io/docs/getting-started/installation/
```

## Development

### Adding New Tests

**E2E Test:**
```typescript
// qa-automation/e2e-tests/tests/new-feature.spec.ts
import { test } from '@playwright/test';
import { HomePage } from '../pages/HomePage';

test('new feature test', async ({ page }) => {
  const homePage = new HomePage(page);
  await homePage.navigate();
  // ... test steps
});
```

**Performance Test:**
```javascript
// qa-automation/performance/scenarios/new-scenario.js
import http from 'k6/http';
import { check } from 'k6';

export default function() {
  const res = http.get(`${__ENV.API_URL}/api/endpoint`);
  check(res, { 'status is 200': (r) => r.status === 200 });
}
```

## Best Practices

1. **Run locally before push**: `./qa-automation/run-all-qa.sh --quick`
2. **Review reports**: Check dashboard after each run
3. **Fix issues promptly**: Don't let quality debt accumulate
4. **Update baselines**: When intentional changes affect metrics
5. **Monitor trends**: Use dashboard to track quality over time

## Maintenance

```bash
# Update dependencies
cd qa-automation/e2e-tests && npm update
pip install --upgrade -r qa-automation/requirements.txt

# Clean old reports
./qa-automation/scripts/cleanup.sh --older-than 7d

# Verify system health
./qa-automation/scripts/health-check.sh
```

## Support

- **Documentation**: See individual component READMEs
- **Issues**: Create GitHub issue with `qa-automation` label
- **Questions**: Check troubleshooting section above

## Roadmap

- [ ] Visual regression testing with Percy/BackstopJS
- [ ] API contract testing with Pact
- [ ] Accessibility testing with axe-core
- [ ] Mobile testing with Appium
- [ ] Chaos engineering tests
- [ ] AI-powered test generation

---

**Built with ❤️ for quality assurance**
