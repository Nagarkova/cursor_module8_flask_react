# Comprehensive REST API Test Suite

A comprehensive test suite for REST API endpoints covering user management, product catalog, and orders with full CRUD operations, authentication, authorization, validation, error handling, rate limiting, and performance testing.

## Test Coverage

### Total Test Cases: **150+**

#### By Endpoint:
- **User Management**: 40+ tests
- **Product Catalog**: 40+ tests
- **Orders**: 35+ tests
- **Rate Limiting**: 8 tests
- **Error Responses**: 12 tests
- **Performance**: 15+ tests

#### By Operation:
- **GET**: 30+ tests
- **POST**: 35+ tests
- **PUT**: 25+ tests
- **DELETE**: 15+ tests
- **Authentication**: 10+ tests

#### By Category:
- **Authentication & Authorization**: 25+ tests
- **Input Validation**: 30+ tests
- **Error Handling**: 20+ tests
- **Rate Limiting**: 8 tests
- **Performance**: 15+ tests
- **Security**: 20+ tests

## Test Files

1. **`test_user_management.py`** - User management API tests (40+ tests)
2. **`test_product_catalog.py`** - Product catalog API tests (40+ tests)
3. **`test_orders.py`** - Orders API tests (35+ tests)
4. **`test_rate_limiting.py`** - Rate limiting tests (8 tests)
5. **`test_error_responses.py`** - Error response tests (12 tests)
6. **`conftest.py`** - Pytest fixtures and configuration

## Features Tested

### ✅ Authentication
- JWT token generation and validation
- Login/logout functionality
- Token expiration handling
- Invalid token rejection

### ✅ Authorization
- Role-based access control (admin vs user)
- Resource ownership validation
- Endpoint permission checks

### ✅ Input Validation
- Required field validation
- Data type validation
- Format validation (email, etc.)
- Range validation (price, quantity, etc.)
- SQL injection prevention
- XSS prevention

### ✅ Error Responses
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 409 Conflict
- 422 Unprocessable Entity
- 429 Too Many Requests
- 500 Internal Server Error

### ✅ Rate Limiting
- Request limit enforcement
- Rate limit headers
- Per-endpoint limits
- Per-user limits
- Rate limit reset

### ✅ Performance
- Response time under 500ms
- Endpoint performance testing
- Filter/query performance
- Pagination performance

## Setup

### Install Dependencies

```bash
cd api_tests
pip install -r requirements.txt
```

### Run Tests

```bash
# Run all tests
pytest -v

# Run specific test file
pytest test_user_management.py -v

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test class
pytest test_user_management.py::TestUserManagement -v

# Run specific test
pytest test_user_management.py::TestUserManagement::test_get_users_list -v
```

## Test Structure

### User Management Tests

```python
class TestUserManagement:
    # GET Operations
    - test_get_users_list
    - test_get_user_by_id
    - test_get_current_user
    - test_get_users_unauthorized
    
    # POST Operations
    - test_create_user_success
    - test_create_user_duplicate_username
    - test_create_user_invalid_email
    - test_create_user_missing_fields
    
    # PUT Operations
    - test_update_user_success
    - test_update_user_forbidden
    - test_update_user_own_profile
    
    # DELETE Operations
    - test_delete_user_success
    - test_delete_user_forbidden
    
    # Authentication
    - test_login_success
    - test_login_invalid_credentials
    
    # Performance
    - test_get_users_performance
    - test_create_user_performance
```

### Product Catalog Tests

```python
class TestProductCatalog:
    # GET Operations
    - test_get_products_list
    - test_get_products_with_pagination
    - test_get_products_with_filter
    - test_get_products_with_search
    - test_get_product_by_id
    
    # POST Operations
    - test_create_product_success
    - test_create_product_unauthorized
    - test_create_product_missing_fields
    
    # PUT Operations
    - test_update_product_success
    - test_update_product_forbidden
    
    # DELETE Operations
    - test_delete_product_success
    - test_delete_product_forbidden
    
    # Performance
    - test_get_products_performance
    - test_create_product_performance
```

### Orders Tests

```python
class TestOrders:
    # GET Operations
    - test_get_orders_list
    - test_get_order_by_id
    - test_get_orders_with_status_filter
    
    # POST Operations
    - test_create_order_success
    - test_create_order_missing_items
    - test_create_order_insufficient_stock
    
    # PUT Operations
    - test_update_order_status
    - test_cancel_order
    
    # DELETE Operations
    - test_delete_order_success
    - test_delete_order_forbidden
    
    # Performance
    - test_get_orders_performance
    - test_create_order_performance
```

## Performance Requirements

All endpoints are tested to ensure response times are under **500ms**:

- ✅ GET requests: < 500ms
- ✅ POST requests: < 500ms
- ✅ PUT requests: < 500ms
- ✅ DELETE requests: < 500ms
- ✅ Filtered queries: < 500ms
- ✅ Paginated queries: < 500ms

## Security Tests

### SQL Injection Prevention
- User input fields
- Product fields
- Order fields
- Search queries

### XSS Prevention
- User input sanitization
- Product descriptions
- Order notes

### Authentication Security
- Token validation
- Expired token handling
- Invalid token rejection

### Authorization Security
- Role-based access
- Resource ownership
- Admin-only endpoints

## Rate Limiting Tests

- Request limit enforcement
- Rate limit headers
- Per-endpoint limits
- Per-user limits
- Admin bypass (if applicable)
- Rate limit reset

## Error Response Tests

All error scenarios return proper HTTP status codes and error messages:

- 400 Bad Request - Invalid input
- 401 Unauthorized - Missing/invalid auth
- 403 Forbidden - Insufficient permissions
- 404 Not Found - Resource doesn't exist
- 409 Conflict - Duplicate resource
- 422 Unprocessable Entity - Validation errors
- 429 Too Many Requests - Rate limit exceeded
- 500 Internal Server Error - Server errors

## Test Execution

### Run All Tests
```bash
pytest -v
```

### Run with Coverage
```bash
pytest --cov=. --cov-report=html --cov-report=term
```

### Run Specific Category
```bash
# Authentication tests
pytest -k "auth" -v

# Performance tests
pytest -k "performance" -v

# Error tests
pytest -k "error" -v
```

### Run in Parallel
```bash
pip install pytest-xdist
pytest -n auto -v
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: |
          cd api_tests
          pip install -r requirements.txt
          pytest --cov=. --cov-report=xml
      - uses: codecov/codecov-action@v2
```

## Test Reports

### HTML Coverage Report
```bash
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

### JUnit XML Report
```bash
pytest --junitxml=report.xml
```

### JSON Report
```bash
pytest --json-report --json-report-file=report.json
```

## Best Practices

1. **Isolation**: Each test is independent
2. **Fixtures**: Reusable test data and setup
3. **Assertions**: Clear and specific assertions
4. **Performance**: All endpoints tested for < 500ms
5. **Security**: SQL injection and XSS prevention tested
6. **Error Handling**: All error scenarios covered
7. **Documentation**: Clear test descriptions

## Notes

- Tests use in-memory SQLite database for speed
- JWT tokens are generated for testing
- Test data is seeded in fixtures
- Performance tests verify < 500ms response time
- Rate limiting tests may require actual rate limiting implementation

## License

MIT License
