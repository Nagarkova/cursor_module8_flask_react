# Test Execution Guide

## Quick Start

### Backend Tests

```bash
cd backend
./run_tests.sh
```

Or manually:

```bash
cd backend
pytest test_checkout.py test_checkout_expanded.py -v
```

### Frontend Tests

```bash
cd frontend
./run_tests.sh
```

Or manually:

```bash
cd frontend
npm test
```

---

## Detailed Test Execution

### Backend Test Suites

#### 1. Original Test Suite (`test_checkout.py`)
**40 test cases** covering:
- Positive scenarios (8 tests)
- Negative scenarios (12 tests)
- Edge cases (9 tests)
- Security scenarios (9 tests)
- Integration tests (2 tests)

```bash
# Run all original tests
pytest test_checkout.py -v

# Run specific category
pytest test_checkout.py::TestPositiveScenarios -v
pytest test_checkout.py::TestNegativeScenarios -v
pytest test_checkout.py::TestEdgeCases -v
pytest test_checkout.py::TestSecurityScenarios -v
pytest test_checkout.py::TestIntegrationScenarios -v
```

#### 2. Expanded Test Suite (`test_checkout_expanded.py`)
**15+ additional test cases** covering:
- Expanded positive scenarios (7 tests)
- Expanded negative scenarios (5 tests)
- Expanded edge cases (7 tests)
- Security & PCI compliance (8 tests)

```bash
# Run all expanded tests
pytest test_checkout_expanded.py -v

# Run specific category
pytest test_checkout_expanded.py::TestPositiveScenariosExpanded -v
pytest test_checkout_expanded.py::TestNegativeScenariosExpanded -v
pytest test_checkout_expanded.py::TestEdgeCasesExpanded -v
pytest test_checkout_expanded.py::TestSecurityAndPCICompliance -v
```

#### 3. Combined Test Execution

```bash
# Run all backend tests
pytest test_checkout.py test_checkout_expanded.py -v

# Run with coverage
pytest test_checkout.py test_checkout_expanded.py \
    --cov=app \
    --cov-report=term-missing \
    --cov-report=html \
    -v

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Frontend Test Suites

#### 1. Component Tests (`App.test.js`)
**20+ test cases** covering:
- App component rendering
- ProductList component
- Cart component
- Checkout component
- OrderConfirmation component

```bash
# Run all component tests
npm test -- App.test.js

# Run in watch mode
npm test -- App.test.js --watch
```

#### 2. Integration Tests (`integration.test.js`)
**5+ test cases** covering:
- Complete checkout flow
- Checkout with discount code
- Error handling scenarios

```bash
# Run integration tests
npm test -- integration.test.js

# Run all frontend tests
npm test
```

#### 3. Frontend Test Coverage

```bash
# Run with coverage
npm test -- --coverage --watchAll=false

# View coverage report
open coverage/lcov-report/index.html  # macOS
```

---

## Test Categories Breakdown

### Positive Test Cases (24 total)

**Backend (17 tests)**
- ✅ Add single item to cart
- ✅ Add multiple different items
- ✅ Get cart with items
- ✅ Apply valid discount code
- ✅ Checkout with valid payment
- ✅ Checkout with PayPal
- ✅ Checkout with discount code
- ✅ Update cart quantity
- ✅ Remove from cart
- ✅ Get order details
- ✅ Checkout with multiple discount codes
- ✅ Checkout with maximum cart items
- ✅ Checkout with large quantity
- ✅ Checkout with different card types
- ✅ Complete checkout flow
- ✅ Stock reduction after checkout
- ✅ Multiple discount code applications

**Frontend (7 tests)**
- ✅ Render app with navigation
- ✅ Switch between views
- ✅ Display product list
- ✅ Add to cart functionality
- ✅ Display cart items
- ✅ Submit checkout form
- ✅ Apply discount code

### Negative Test Cases (21 total)

**Backend (16 tests)**
- ❌ Missing session_id
- ❌ Missing product_id
- ❌ Nonexistent product
- ❌ Invalid quantity
- ❌ Invalid discount code
- ❌ Inactive discount code
- ❌ Expired discount code
- ❌ Invalid email
- ❌ Invalid card number
- ❌ Invalid CVV
- ❌ Payment declined
- ❌ Expired card
- ❌ Invalid discount format
- ❌ Missing payment method
- ❌ Malformed JSON
- ❌ Nonexistent order

**Frontend (5 tests)**
- ❌ Invalid email format
- ❌ Discount code error
- ❌ Checkout error
- ❌ Out of stock display
- ❌ API error handling

### Edge Cases (19 total)

**Backend (16 tests)**
- 🔍 Empty cart checkout
- 🔍 Discount on empty cart
- 🔍 Exceeds stock
- 🔍 Out of stock product
- 🔍 Empty cart display
- 🔍 Multiple same product
- 🔍 Update exceeds stock
- 🔍 Remove nonexistent item
- 🔍 Missing required fields
- 🔍 Cart maximum items
- 🔍 Concurrent add to cart
- 🔍 Concurrent checkout
- 🔍 Cart total precision
- 🔍 Discount on zero total
- 🔍 Exactly available stock
- 🔍 Very long address

**Frontend (3 tests)**
- 🔍 Empty cart message
- 🔍 Out of stock handling
- 🔍 Network error handling

### Security & PCI Compliance (19 total)

**Backend (16 tests)**
- 🔒 SQL injection in session_id
- 🔒 SQL injection in discount code
- 🔒 SQL injection in email
- 🔒 SQL injection in all fields
- 🔒 XSS in shipping address
- 🔒 XSS in all text fields
- 🔒 PCI: Card number masking
- 🔒 PCI: CVV not stored
- 🔒 PCI: Payment data encryption
- 🔒 PCI: Rate limiting
- 🔒 Input length limits
- 🔒 Cross-session access
- 🔒 Special characters
- 🔒 Payment data validation
- 🔒 CVV validation
- 🔒 Email validation

**Frontend (3 tests)**
- 🔒 Input sanitization
- 🔒 XSS prevention
- 🔒 Secure API calls

### Integration Tests (6 total)

**Backend (2 tests)**
- 🔗 Complete checkout flow
- 🔗 Stock reduction

**Frontend (4 tests)**
- 🔗 Complete checkout flow
- 🔗 Checkout with discount
- 🔗 Out of stock error
- 🔗 Invalid discount error

---

## Test Execution Examples

### Run Specific Test

```bash
# Backend
pytest test_checkout.py::TestPositiveScenarios::test_add_item_to_cart_success -v

# Frontend
npm test -- -t "renders app header"
```

### Run Tests Matching Pattern

```bash
# Backend - all checkout tests
pytest test_checkout.py -k "checkout" -v

# Frontend - all cart tests
npm test -- -t "cart"
```

### Run Tests in Parallel (Backend)

```bash
pip install pytest-xdist
pytest test_checkout.py test_checkout_expanded.py -n auto
```

### Generate Test Report

```bash
# Backend - HTML report
pytest test_checkout.py test_checkout_expanded.py \
    --html=report.html \
    --self-contained-html

# Frontend - JSON report
npm test -- --json --outputFile=test-results.json
```

---

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: |
          cd backend
          pip install -r requirements.txt
          pytest test_checkout.py test_checkout_expanded.py --cov=app --cov-report=xml
      - uses: codecov/codecov-action@v2

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: |
          cd frontend
          npm install
          npm test -- --coverage --watchAll=false
```

---

## Test Data Generation

The test suite includes a `TestDataGenerator` class for generating realistic test data:

```python
from test_data_generator import TestDataGenerator

# Generate test data
session_id = TestDataGenerator.generate_session_id()
email = TestDataGenerator.generate_email()
card_number = TestDataGenerator.generate_card_number(valid=True)
checkout_data = TestDataGenerator.generate_checkout_data(session_id)
```

See `test_data_generator.py` for all available methods.

---

## Troubleshooting

### Backend Tests

**Issue**: Import errors
```bash
# Ensure you're in the backend directory
cd backend
# Activate virtual environment
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```

**Issue**: Database errors
```bash
# Tests use in-memory SQLite, should work automatically
# If issues persist, check SQLAlchemy version compatibility
```

### Frontend Tests

**Issue**: Module not found
```bash
# Install dependencies
npm install
# Clear cache
npm test -- --clearCache
```

**Issue**: Axios mock not working
```bash
# Ensure axios is properly mocked in test files
# Check that jest.mock('axios') is at the top of test files
```

---

## Performance Considerations

### Test Execution Time

- **Backend**: ~5-10 seconds for all tests
- **Frontend**: ~10-15 seconds for all tests
- **Total**: ~15-25 seconds for complete suite

### Optimization Tips

1. Use `-x` flag to stop on first failure
2. Use `-k` to run specific tests
3. Use `pytest-xdist` for parallel execution
4. Use `--lf` to run last failed tests first

```bash
# Stop on first failure
pytest test_checkout.py -x

# Run only failed tests from last run
pytest test_checkout.py --lf

# Run tests matching keyword
pytest test_checkout.py -k "checkout" -v
```

---

## Test Maintenance

### Adding New Tests

1. Identify the appropriate test file
2. Add test to relevant test class
3. Use `TestDataGenerator` for test data
4. Follow naming convention: `test_<feature>_<scenario>`
5. Add docstring explaining test purpose
6. Run tests to verify

### Updating Tests

1. Run tests to identify failures
2. Update test data if needed
3. Adjust assertions if behavior changed
4. Verify all tests still pass

---

## Summary

- **Total Test Cases**: 80+
- **Backend Tests**: 55+
- **Frontend Tests**: 25+
- **Test Categories**: 5 (Positive, Negative, Edge Cases, Security, Integration)
- **Coverage**: 90%+ for critical paths

For detailed test documentation, see `TEST_SUITE_SUMMARY.md` and `TEST_CASES.md`.
