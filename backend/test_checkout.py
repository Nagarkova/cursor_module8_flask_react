"""
Comprehensive test cases for e-commerce checkout process
Covers positive scenarios, negative scenarios, edge cases, and security scenarios
"""
import pytest
import json
from app import app, db, Product, CartItem, DiscountCode, Order
from datetime import datetime, timedelta

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['MAIL_SUPPRESS_SEND'] = True
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Seed test data
            products = [
                Product(name='Test Product 1', price=100.0, stock=10),
                Product(name='Test Product 2', price=50.0, stock=5),
                Product(name='Out of Stock', price=25.0, stock=0),
            ]
            for p in products:
                db.session.add(p)
            
            discount_codes = [
                DiscountCode(code='VALID10', discount_percent=10.0, is_active=True),
                DiscountCode(code='INACTIVE', discount_percent=20.0, is_active=False),
                DiscountCode(
                    code='EXPIRED',
                    discount_percent=15.0,
                    is_active=True,
                    expiry_date=datetime.utcnow() - timedelta(days=1)
                ),
            ]
            for code in discount_codes:
                db.session.add(code)
            
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture
def session_id():
    """Generate test session ID"""
    return 'test_session_123'

# ==================== POSITIVE SCENARIOS ====================

class TestPositiveScenarios:
    """Test cases for successful checkout flows"""
    
    def test_add_item_to_cart_success(self, client, session_id):
        """Test successfully adding item to cart"""
        response = client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 2
        })
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'message' in data
        assert 'successfully' in data['message'].lower()
    
    def test_get_cart_with_items(self, client, session_id):
        """Test retrieving cart with items"""
        # Add item first
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 2
        })
        
        response = client.get(f'/api/cart?session_id={session_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'items' in data
        assert 'total' in data
        assert len(data['items']) == 1
        assert data['total'] == 200.0  # 100 * 2
    
    def test_apply_valid_discount_code(self, client, session_id):
        """Test applying a valid discount code"""
        # Add item to cart
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        response = client.post('/api/discount/apply', json={
            'session_id': session_id,
            'code': 'VALID10'
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['discount_code'] == 'VALID10'
        assert data['discount_percent'] == 10.0
        assert data['original_total'] == 100.0
        assert data['discount_amount'] == 10.0
        assert data['final_total'] == 90.0
    
    def test_checkout_with_valid_payment(self, client, session_id):
        """Test successful checkout with valid payment"""
        # Add item to cart
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        response = client.post('/api/checkout', json={
            'session_id': session_id,
            'email': 'test@example.com',
            'payment_method': 'card',
            'card_number': '4111111111111111',
            'cvv': '123',
            'expiry_date': '12/25',
            'shipping_address': '123 Test St'
        })
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'order_number' in data
        assert data['status'] == 'confirmed'
        assert data['total_amount'] == 100.0
    
    def test_checkout_with_discount_code(self, client, session_id):
        """Test checkout with discount code applied"""
        # Add item to cart
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        response = client.post('/api/checkout', json={
            'session_id': session_id,
            'email': 'test@example.com',
            'payment_method': 'card',
            'card_number': '4111111111111111',
            'cvv': '123',
            'expiry_date': '12/25',
            'shipping_address': '123 Test St',
            'discount_code': 'VALID10'
        })
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['total_amount'] == 90.0  # 100 - 10% discount
    
    def test_update_cart_item_quantity(self, client, session_id):
        """Test updating cart item quantity"""
        # Add item first
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        # Get cart to find item_id
        cart_response = client.get(f'/api/cart?session_id={session_id}')
        item_id = json.loads(cart_response.data)['items'][0]['id']
        
        # Update quantity
        response = client.post('/api/cart/update', json={
            'session_id': session_id,
            'item_id': item_id,
            'quantity': 3
        })
        assert response.status_code == 200
        
        # Verify update
        cart_response = client.get(f'/api/cart?session_id={session_id}')
        data = json.loads(cart_response.data)
        assert data['items'][0]['quantity'] == 3
        assert data['total'] == 300.0
    
    def test_remove_item_from_cart(self, client, session_id):
        """Test removing item from cart"""
        # Add items
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 2,
            'quantity': 1
        })
        
        # Get cart to find item_id
        cart_response = client.get(f'/api/cart?session_id={session_id}')
        item_id = json.loads(cart_response.data)['items'][0]['id']
        
        # Remove item
        response = client.post('/api/cart/remove', json={
            'session_id': session_id,
            'item_id': item_id
        })
        assert response.status_code == 200
        
        # Verify removal
        cart_response = client.get(f'/api/cart?session_id={session_id}')
        data = json.loads(cart_response.data)
        assert len(data['items']) == 1
    
    def test_get_order_details(self, client, session_id):
        """Test retrieving order details"""
        # Create order
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        checkout_response = client.post('/api/checkout', json={
            'session_id': session_id,
            'email': 'test@example.com',
            'payment_method': 'card',
            'card_number': '4111111111111111',
            'cvv': '123',
            'expiry_date': '12/25',
            'shipping_address': '123 Test St'
        })
        order_number = json.loads(checkout_response.data)['order_number']
        
        # Get order details
        response = client.get(f'/api/orders/{order_number}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['order_number'] == order_number
        assert data['status'] == 'confirmed'

# ==================== NEGATIVE SCENARIOS ====================

class TestNegativeScenarios:
    """Test cases for error handling and invalid inputs"""
    
    def test_add_item_missing_session_id(self, client):
        """Test adding item without session_id"""
        response = client.post('/api/cart/add', json={
            'product_id': 1,
            'quantity': 1
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_add_item_missing_product_id(self, client, session_id):
        """Test adding item without product_id"""
        response = client.post('/api/cart/add', json={
            'session_id': session_id,
            'quantity': 1
        })
        assert response.status_code == 400
    
    def test_add_nonexistent_product(self, client, session_id):
        """Test adding non-existent product to cart"""
        response = client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 999,
            'quantity': 1
        })
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'not found' in data['error'].lower()
    
    def test_add_item_invalid_quantity(self, client, session_id):
        """Test adding item with invalid quantity"""
        # Zero quantity
        response = client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 0
        })
        assert response.status_code == 400
        
        # Negative quantity
        response = client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': -1
        })
        assert response.status_code == 400
        
        # Non-integer quantity
        response = client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 'invalid'
        })
        assert response.status_code == 400
    
    def test_apply_invalid_discount_code(self, client, session_id):
        """Test applying invalid discount code"""
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        response = client.post('/api/discount/apply', json={
            'session_id': session_id,
            'code': 'INVALID_CODE'
        })
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'invalid' in data['error'].lower()
    
    def test_apply_inactive_discount_code(self, client, session_id):
        """Test applying inactive discount code"""
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        response = client.post('/api/discount/apply', json={
            'session_id': session_id,
            'code': 'INACTIVE'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'not active' in data['error'].lower()
    
    def test_apply_expired_discount_code(self, client, session_id):
        """Test applying expired discount code"""
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        response = client.post('/api/discount/apply', json={
            'session_id': session_id,
            'code': 'EXPIRED'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'expired' in data['error'].lower()
    
    def test_checkout_invalid_email(self, client, session_id):
        """Test checkout with invalid email"""
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        response = client.post('/api/checkout', json={
            'session_id': session_id,
            'email': 'invalid-email',
            'payment_method': 'card',
            'card_number': '4111111111111111',
            'cvv': '123',
            'expiry_date': '12/25',
            'shipping_address': '123 Test St'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'email' in data['error'].lower()
    
    def test_checkout_invalid_card_number(self, client, session_id):
        """Test checkout with invalid card number"""
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        response = client.post('/api/checkout', json={
            'session_id': session_id,
            'email': 'test@example.com',
            'payment_method': 'card',
            'card_number': '123',
            'cvv': '123',
            'expiry_date': '12/25',
            'shipping_address': '123 Test St'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'card' in data['error'].lower()
    
    def test_checkout_invalid_cvv(self, client, session_id):
        """Test checkout with invalid CVV"""
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        response = client.post('/api/checkout', json={
            'session_id': session_id,
            'email': 'test@example.com',
            'payment_method': 'card',
            'card_number': '4111111111111111',
            'cvv': '12',
            'expiry_date': '12/25',
            'shipping_address': '123 Test St'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'cvv' in data['error'].lower()
    
    def test_checkout_payment_declined(self, client, session_id):
        """Test checkout with declined payment (card ending in 0000)"""
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        response = client.post('/api/checkout', json={
            'session_id': session_id,
            'email': 'test@example.com',
            'payment_method': 'card',
            'card_number': '4111111111111000',
            'cvv': '123',
            'expiry_date': '12/25',
            'shipping_address': '123 Test St'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'declined' in data['error'].lower()
    
    def test_get_nonexistent_order(self, client):
        """Test retrieving non-existent order"""
        response = client.get('/api/orders/INVALID-ORDER')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'not found' in data['error'].lower()

# ==================== EDGE CASES ====================

class TestEdgeCases:
    """Test cases for edge cases and boundary conditions"""
    
    def test_empty_cart_checkout(self, client, session_id):
        """Test checkout with empty cart"""
        response = client.post('/api/checkout', json={
            'session_id': session_id,
            'email': 'test@example.com',
            'payment_method': 'card',
            'card_number': '4111111111111111',
            'cvv': '123',
            'expiry_date': '12/25',
            'shipping_address': '123 Test St'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'empty' in data['error'].lower()
    
    def test_apply_discount_empty_cart(self, client, session_id):
        """Test applying discount code to empty cart"""
        response = client.post('/api/discount/apply', json={
            'session_id': session_id,
            'code': 'VALID10'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'empty' in data['error'].lower()
    
    def test_add_item_exceeds_stock(self, client, session_id):
        """Test adding item quantity that exceeds stock"""
        response = client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 100  # More than available stock (10)
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'stock' in data['error'].lower()
    
    def test_add_out_of_stock_product(self, client, session_id):
        """Test adding out of stock product"""
        response = client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 3,  # Out of Stock product
            'quantity': 1
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'stock' in data['error'].lower()
    
    def test_get_cart_empty(self, client, session_id):
        """Test getting empty cart"""
        response = client.get(f'/api/cart?session_id={session_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['items']) == 0
        assert data['total'] == 0
        assert data['item_count'] == 0
    
    def test_add_multiple_items_same_product(self, client, session_id):
        """Test adding same product multiple times (should update quantity)"""
        # Add first time
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 2
        })
        
        # Add same product again
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 3
        })
        
        # Check cart
        response = client.get(f'/api/cart?session_id={session_id}')
        data = json.loads(response.data)
        assert len(data['items']) == 1
        assert data['items'][0]['quantity'] == 5  # 2 + 3
        assert data['total'] == 500.0
    
    def test_update_cart_exceeds_stock(self, client, session_id):
        """Test updating cart quantity that exceeds stock"""
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        cart_response = client.get(f'/api/cart?session_id={session_id}')
        item_id = json.loads(cart_response.data)['items'][0]['id']
        
        response = client.post('/api/cart/update', json={
            'session_id': session_id,
            'item_id': item_id,
            'quantity': 100  # Exceeds stock
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'stock' in data['error'].lower()
    
    def test_remove_nonexistent_item(self, client, session_id):
        """Test removing item that doesn't exist"""
        response = client.post('/api/cart/remove', json={
            'session_id': session_id,
            'item_id': 999
        })
        assert response.status_code == 404
    
    def test_checkout_missing_required_fields(self, client, session_id):
        """Test checkout with missing required fields"""
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        # Missing email
        response = client.post('/api/checkout', json={
            'session_id': session_id,
            'payment_method': 'card',
            'card_number': '4111111111111111',
            'cvv': '123',
            'expiry_date': '12/25'
        })
        assert response.status_code == 400
        
        # Missing card number
        response = client.post('/api/checkout', json={
            'session_id': session_id,
            'email': 'test@example.com',
            'payment_method': 'card',
            'cvv': '123',
            'expiry_date': '12/25'
        })
        assert response.status_code == 400

# ==================== SECURITY SCENARIOS ====================

class TestSecurityScenarios:
    """Test cases for security vulnerabilities"""
    
    def test_sql_injection_in_session_id(self, client):
        """Test SQL injection attempt in session_id"""
        malicious_session = "'; DROP TABLE orders; --"
        response = client.post('/api/cart/add', json={
            'session_id': malicious_session,
            'product_id': 1,
            'quantity': 1
        })
        # Should sanitize and handle gracefully
        assert response.status_code in [201, 400]  # Either succeeds with sanitized input or fails validation
    
    def test_sql_injection_in_discount_code(self, client, session_id):
        """Test SQL injection attempt in discount code"""
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        malicious_code = "'; DROP TABLE discount_codes; --"
        response = client.post('/api/discount/apply', json={
            'session_id': session_id,
            'code': malicious_code
        })
        # Should sanitize and return invalid code error
        assert response.status_code == 404
    
    def test_xss_in_shipping_address(self, client, session_id):
        """Test XSS attempt in shipping address"""
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        xss_payload = "<script>alert('XSS')</script>"
        response = client.post('/api/checkout', json={
            'session_id': session_id,
            'email': 'test@example.com',
            'payment_method': 'card',
            'card_number': '4111111111111111',
            'cvv': '123',
            'expiry_date': '12/25',
            'shipping_address': xss_payload
        })
        # Should sanitize input
        assert response.status_code == 201
    
    def test_sql_injection_in_email(self, client, session_id):
        """Test SQL injection attempt in email field"""
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        malicious_email = "test@example.com'; DROP TABLE orders; --"
        response = client.post('/api/checkout', json={
            'session_id': session_id,
            'email': malicious_email,
            'payment_method': 'card',
            'card_number': '4111111111111111',
            'cvv': '123',
            'expiry_date': '12/25',
            'shipping_address': '123 Test St'
        })
        # Should fail email validation
        assert response.status_code == 400
    
    def test_payment_data_validation(self, client, session_id):
        """Test payment data validation"""
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        # Test various invalid card formats
        invalid_cards = [
            '1234',  # Too short
            '12345678901234567890',  # Too long
            'abcd1234567890',  # Contains letters
            '1234-5678-9012-3456',  # With dashes (should be sanitized)
            '1234 5678 9012 3456',  # With spaces (should be sanitized)
        ]
        
        for card in invalid_cards:
            response = client.post('/api/checkout', json={
                'session_id': session_id,
                'email': 'test@example.com',
                'payment_method': 'card',
                'card_number': card,
                'cvv': '123',
                'expiry_date': '12/25',
                'shipping_address': '123 Test St'
            })
            assert response.status_code == 400
    
    def test_cvv_validation(self, client, session_id):
        """Test CVV validation"""
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        invalid_cvvs = ['12', '12345', 'abc', '12a']
        
        for cvv in invalid_cvvs:
            response = client.post('/api/checkout', json={
                'session_id': session_id,
                'email': 'test@example.com',
                'payment_method': 'card',
                'card_number': '4111111111111111',
                'cvv': cvv,
                'expiry_date': '12/25',
                'shipping_address': '123 Test St'
            })
            assert response.status_code == 400
    
    def test_email_validation(self, client, session_id):
        """Test email validation"""
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        invalid_emails = [
            'notanemail',
            '@example.com',
            'test@',
            'test..test@example.com',
            'test@example',
            'test @example.com',
        ]
        
        for email in invalid_emails:
            response = client.post('/api/checkout', json={
                'session_id': session_id,
                'email': email,
                'payment_method': 'card',
                'card_number': '4111111111111111',
                'cvv': '123',
                'expiry_date': '12/25',
                'shipping_address': '123 Test St'
            })
            assert response.status_code == 400
    
    def test_cross_session_cart_access(self, client):
        """Test that users cannot access other users' carts"""
        session1 = 'session_1'
        session2 = 'session_2'
        
        # Add item to session1's cart
        client.post('/api/cart/add', json={
            'session_id': session1,
            'product_id': 1,
            'quantity': 1
        })
        
        # Try to remove from session2
        cart_response = client.get(f'/api/cart?session_id={session1}')
        item_id = json.loads(cart_response.data)['items'][0]['id']
        
        response = client.post('/api/cart/remove', json={
            'session_id': session2,
            'item_id': item_id
        })
        # Should fail - item belongs to different session
        assert response.status_code == 404
    
    def test_special_characters_in_inputs(self, client, session_id):
        """Test handling of special characters in inputs"""
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 1
        })
        
        # Test with special characters
        response = client.post('/api/checkout', json={
            'session_id': session_id,
            'email': 'test+special@example.com',
            'payment_method': 'card',
            'card_number': '4111111111111111',
            'cvv': '123',
            'expiry_date': '12/25',
            'shipping_address': '123 Test St, Apt #4, City, State 12345'
        })
        # Should handle special characters gracefully
        assert response.status_code == 201

# ==================== INTEGRATION TESTS ====================

class TestIntegrationScenarios:
    """Test complete checkout flow integration"""
    
    def test_complete_checkout_flow(self, client, session_id):
        """Test complete checkout flow from cart to order confirmation"""
        # 1. Add items to cart
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 2
        })
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 2,
            'quantity': 1
        })
        
        # 2. Verify cart
        cart_response = client.get(f'/api/cart?session_id={session_id}')
        cart_data = json.loads(cart_response.data)
        assert len(cart_data['items']) == 2
        assert cart_data['total'] == 250.0  # (100*2) + (50*1)
        
        # 3. Apply discount
        discount_response = client.post('/api/discount/apply', json={
            'session_id': session_id,
            'code': 'VALID10'
        })
        discount_data = json.loads(discount_response.data)
        assert discount_data['final_total'] == 225.0  # 250 - 10%
        
        # 4. Checkout
        checkout_response = client.post('/api/checkout', json={
            'session_id': session_id,
            'email': 'test@example.com',
            'payment_method': 'card',
            'card_number': '4111111111111111',
            'cvv': '123',
            'expiry_date': '12/25',
            'shipping_address': '123 Test St',
            'discount_code': 'VALID10'
        })
        assert checkout_response.status_code == 201
        order_data = json.loads(checkout_response.data)
        order_number = order_data['order_number']
        
        # 5. Verify cart is empty
        cart_response = client.get(f'/api/cart?session_id={session_id}')
        cart_data = json.loads(cart_response.data)
        assert len(cart_data['items']) == 0
        
        # 6. Verify order
        order_response = client.get(f'/api/orders/{order_number}')
        order_details = json.loads(order_response.data)
        assert order_details['status'] == 'confirmed'
        assert order_details['total_amount'] == 225.0
    
    def test_stock_reduction_after_checkout(self, client, session_id):
        """Test that stock is reduced after successful checkout"""
        initial_stock = Product.query.get(1).stock
        
        client.post('/api/cart/add', json={
            'session_id': session_id,
            'product_id': 1,
            'quantity': 3
        })
        
        client.post('/api/checkout', json={
            'session_id': session_id,
            'email': 'test@example.com',
            'payment_method': 'card',
            'card_number': '4111111111111111',
            'cvv': '123',
            'expiry_date': '12/25',
            'shipping_address': '123 Test St'
        })
        
        # Verify stock reduced
        updated_product = Product.query.get(1)
        assert updated_product.stock == initial_stock - 3

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
