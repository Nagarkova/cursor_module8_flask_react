# QA Automation - Quick Reference

## ⚡ Quick Start

```bash
# 1. Setup (one-time)
cd qa-automation
./setup.sh

# 2. Run all checks
./run-all-qa.sh

# 3. View results
open reports/dashboard.html
```

## 🎯 Common Commands

### Run Everything
```bash
./qa-automation/run-all-qa.sh                    # Full comprehensive scan
./qa-automation/run-all-qa.sh --quick            # Skip performance tests
./qa-automation/run-all-qa.sh --skip-security    # Skip security scans
```

### Run Individual Components
```bash
# E2E Tests
cd qa-automation/e2e-tests
npm test                              # All browsers
npm test -- --headed                  # With browser UI
npm test -- --project=chromium        # Chrome only
npm test -- --debug                   # Debug mode
npm test -- --ui                      # Interactive UI

# Code Quality
./qa-automation/code-quality/run-quality-checks.sh

# Security
./qa-automation/security/run-security-scan.sh

# Performance
./qa-automation/performance/run-performance-tests.sh
```

## 📊 Reports Location

```
qa-automation/reports/
├── dashboard.html                    # Main dashboard ⭐
├── test-results/
│   └── playwright-report/index.html  # E2E tests
├── code-quality/
│   └── quality-report.html           # Code quality
├── security/
│   └── security-report.html          # Security
└── performance/
    └── performance-report.html       # Performance
```

## 🎨 Quality Gates

| Check | Pass Threshold |
|-------|---------------|
| Code Quality | ≥ 6.0/10 |
| Security (High) | 0 issues |
| Security (Medium) | ≤ 5 issues |
| E2E Tests | 100% pass |
| Performance P95 | ≤ 2000ms |

## 🔧 Configuration

### Environment Variables (.env)
```bash
BASE_URL=http://localhost:3000
API_URL=http://localhost:5001
SNYK_TOKEN=your_token
```

### Setup Snyk
```bash
npm install -g snyk
snyk auth
```

### Setup k6
```bash
# macOS
brew install k6

# Linux
sudo apt install k6
```

## 📝 Adding Tests

### New E2E Test
```typescript
// qa-automation/e2e-tests/tests/my-test.spec.ts
import { test } from '@playwright/test';
import { HomePage } from '../pages/HomePage';

test('my test', async ({ page }) => {
  const home = new HomePage(page);
  await home.navigate();
  // test steps
});
```

### New Page Object
```typescript
// qa-automation/e2e-tests/pages/MyPage.ts
import { Page, Locator } from '@playwright/test';
import { BasePage } from './BasePage';

export class MyPage extends BasePage {
  private readonly myButton: Locator;
  
  constructor(page: Page) {
    super(page);
    this.myButton = page.locator('button.my-btn');
  }
  
  async clickMyButton() {
    await this.myButton.click();
  }
}
```

### New Performance Test
```javascript
// qa-automation/performance/scenarios/my-test.js
import http from 'k6/http';

export const options = {
  stages: [{ duration: '1m', target: 50 }],
};

export default function() {
  http.get(`${__ENV.API_URL}/api/endpoint`);
}
```

## 🐛 Troubleshooting

### E2E Tests Failing
```bash
# Check if app is running
./start_app.sh

# Run with UI to see what's happening
cd qa-automation/e2e-tests
npm test -- --headed

# Debug specific test
npm test -- checkout-flow.spec.ts --debug
```

### k6 Not Found
```bash
# macOS
brew install k6

# Check installation
k6 version
```

### Snyk Auth Issues
```bash
# Re-authenticate
snyk auth

# Test authentication
snyk test --help
```

## 📈 CI/CD Integration

### GitHub Actions
```yaml
jobs:
  qa:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup QA
        run: cd qa-automation && ./setup.sh
      - name: Run QA
        run: ./qa-automation/run-all-qa.sh
      - name: Upload Reports
        uses: actions/upload-artifact@v4
        with:
          name: qa-reports
          path: qa-automation/reports/
```

## 🎯 Best Practices

1. **Run locally before push**: `./run-all-qa.sh --quick`
2. **Review reports**: Check dashboard after each run
3. **Fix issues promptly**: Don't accumulate quality debt
4. **Update tests**: Keep tests in sync with features
5. **Monitor trends**: Track quality metrics over time

## 📚 Documentation

- **Full Docs**: `qa-automation/README.md`
- **Summary**: `QA_AUTOMATION_SUMMARY.md`
- **This Card**: `QA_QUICK_REFERENCE.md`

## 🚀 Performance Tips

- Use `--quick` for daily checks
- Run full suite before merging PRs
- Parallel execution is automatic
- Cache is enabled for npm/playwright

## 📞 Support

**Issue Categories:**
- Tests failing → Check application is running
- Tools missing → Run `./setup.sh` again
- Reports not generating → Check permissions on scripts
- Performance slow → Reduce concurrent users in scenarios

---

**Pro Tip**: Bookmark `qa-automation/reports/dashboard.html` for quick access to latest results!
