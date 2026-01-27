# Comprehensive Test Cases for E-Commerce Checkout Process

This document provides a detailed overview of all test cases implemented in the test suite.

## Test Statistics

- **Total Test Cases**: 50+
- **Test Classes**: 5
- **Coverage Areas**: Positive scenarios, Negative scenarios, Edge cases, Security scenarios, Integration tests

---

## 1. Positive Scenarios (TestPositiveScenarios)

Tests for successful checkout flows and expected behavior.

### 1.1 Cart Operations
- ✅ **test_add_item_to_cart_success**: Successfully add item to cart
- ✅ **test_get_cart_with_items**: Retrieve cart with items
- ✅ **test_update_cart_item_quantity**: Update cart item quantity
- ✅ **test_remove_item_from_cart**: Remove item from cart
- ✅ **test_add_multiple_items_same_product**: Add same product multiple times (updates quantity)

### 1.2 Discount Code Operations
- ✅ **test_apply_valid_discount_code**: Apply valid discount code
- ✅ **test_checkout_with_discount_code**: Complete checkout with discount applied

### 1.3 Checkout Operations
- ✅ **test_checkout_with_valid_payment**: Successful checkout with valid payment
- ✅ **test_get_order_details**: Retrieve order details after checkout

---

## 2. Negative Scenarios (TestNegativeScenarios)

Tests for error handling and invalid inputs.

### 2.1 Cart Error Handling
- ❌ **test_add_item_missing_session_id**: Add item without session_id
- ❌ **test_add_item_missing_product_id**: Add item without product_id
- ❌ **test_add_nonexistent_product**: Add non-existent product
- ❌ **test_add_item_invalid_quantity**: Add item with invalid quantity (zero, negative, non-integer)

### 2.2 Discount Code Error Handling
- ❌ **test_apply_invalid_discount_code**: Apply non-existent discount code
- ❌ **test_apply_inactive_discount_code**: Apply inactive discount code
- ❌ **test_apply_expired_discount_code**: Apply expired discount code

### 2.3 Checkout Error Handling
- ❌ **test_checkout_invalid_email**: Checkout with invalid email format
- ❌ **test_checkout_invalid_card_number**: Checkout with invalid card number
- ❌ **test_checkout_invalid_cvv**: Checkout with invalid CVV
- ❌ **test_checkout_payment_declined**: Checkout with declined payment (card ending in 0000)
- ❌ **test_get_nonexistent_order**: Retrieve non-existent order

---

## 3. Edge Cases (TestEdgeCases)

Tests for boundary conditions and unusual scenarios.

### 3.1 Empty Cart Scenarios
- 🔍 **test_empty_cart_checkout**: Attempt checkout with empty cart
- 🔍 **test_apply_discount_empty_cart**: Apply discount code to empty cart
- 🔍 **test_get_cart_empty**: Retrieve empty cart

### 3.2 Stock Management
- 🔍 **test_add_item_exceeds_stock**: Add item quantity exceeding available stock
- 🔍 **test_add_out_of_stock_product**: Add completely out-of-stock product
- 🔍 **test_update_cart_exceeds_stock**: Update cart quantity exceeding stock

### 3.3 Cart Operations Edge Cases
- 🔍 **test_add_multiple_items_same_product**: Add same product multiple times
- 🔍 **test_remove_nonexistent_item**: Remove item that doesn't exist
- 🔍 **test_checkout_missing_required_fields**: Checkout with missing required fields

---

## 4. Security Scenarios (TestSecurityScenarios)

Tests for security vulnerabilities and data validation.

### 4.1 SQL Injection Prevention
- 🔒 **test_sql_injection_in_session_id**: SQL injection attempt in session_id
- 🔒 **test_sql_injection_in_discount_code**: SQL injection attempt in discount code
- 🔒 **test_sql_injection_in_email**: SQL injection attempt in email field

### 4.2 XSS Prevention
- 🔒 **test_xss_in_shipping_address**: XSS attempt in shipping address

### 4.3 Payment Data Validation
- 🔒 **test_payment_data_validation**: Validate various invalid card formats
  - Too short card numbers
  - Too long card numbers
  - Cards with letters
  - Cards with dashes/spaces (should be sanitized)

### 4.4 CVV Validation
- 🔒 **test_cvv_validation**: Validate CVV format
  - Too short CVV
  - Too long CVV
  - CVV with letters
  - Invalid CVV formats

### 4.5 Email Validation
- 🔒 **test_email_validation**: Validate email format
  - Invalid email formats
  - Missing @ symbol
  - Invalid domain formats

### 4.6 Access Control
- 🔒 **test_cross_session_cart_access**: Prevent access to other users' carts

### 4.7 Input Sanitization
- 🔒 **test_special_characters_in_inputs**: Handle special characters in inputs

---

## 5. Integration Tests (TestIntegrationScenarios)

Tests for complete end-to-end workflows.

### 5.1 Complete Checkout Flow
- 🔗 **test_complete_checkout_flow**: 
  - Add multiple items to cart
  - Verify cart contents
  - Apply discount code
  - Complete checkout
  - Verify cart is empty after checkout
  - Verify order details

### 5.2 Stock Management Integration
- 🔗 **test_stock_reduction_after_checkout**: 
  - Verify stock is reduced after successful checkout
  - Ensure stock consistency

---

## Test Coverage Breakdown

### By Category
- **Positive Scenarios**: 8 tests
- **Negative Scenarios**: 12 tests
- **Edge Cases**: 9 tests
- **Security Scenarios**: 9 tests
- **Integration Tests**: 2 tests

### By Feature
- **Cart Operations**: 15+ tests
- **Discount Codes**: 5+ tests
- **Checkout Process**: 12+ tests
- **Payment Validation**: 8+ tests
- **Security**: 9+ tests
- **Order Management**: 3+ tests

---

## Running Specific Test Suites

```bash
# Run all positive scenario tests
pytest test_checkout.py::TestPositiveScenarios -v

# Run all negative scenario tests
pytest test_checkout.py::TestNegativeScenarios -v

# Run all edge case tests
pytest test_checkout.py::TestEdgeCases -v

# Run all security tests
pytest test_checkout.py::TestSecurityScenarios -v

# Run all integration tests
pytest test_checkout.py::TestIntegrationScenarios -v

# Run specific test
pytest test_checkout.py::TestPositiveScenarios::test_add_item_to_cart_success -v
```

---

## Test Data Setup

Each test uses a fresh in-memory database with the following seed data:

### Products
- Test Product 1: $100.00, Stock: 10
- Test Product 2: $50.00, Stock: 5
- Out of Stock: $25.00, Stock: 0

### Discount Codes
- VALID10: 10% discount, Active
- INACTIVE: 20% discount, Inactive
- EXPIRED: 15% discount, Active but expired

---

## Security Test Details

### SQL Injection Patterns Tested
- `'; DROP TABLE orders; --`
- `'; DROP TABLE discount_codes; --`
- SQL keywords: SELECT, INSERT, UPDATE, DELETE, DROP, CREATE, ALTER

### XSS Patterns Tested
- `<script>alert('XSS')</script>`
- HTML injection attempts

### Payment Validation Patterns
- Card numbers: 13-19 digits required
- CVV: 3-4 digits required
- Special characters sanitization
- Format validation (spaces, dashes)

---

## Notes

- All tests use isolated test fixtures with in-memory SQLite database
- Tests are designed to be independent and can run in any order
- Email functionality is mocked during testing (MAIL_SUPPRESS_SEND = True)
- Session isolation is tested to prevent cross-user access
- Input sanitization is tested for all user-provided fields
