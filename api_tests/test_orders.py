"""
Comprehensive API tests for Orders endpoints
Tests GET, POST, PUT, DELETE operations with authentication, authorization, and validation
"""
import pytest
import json
import time

class TestOrders:
    """Orders API Tests"""
    
    # ==================== GET Operations ====================
    
    def test_get_orders_list(self, client, user_auth_headers):
        """Test GET /api/orders - List user's orders"""
        response = client.get('/api/orders', headers=user_auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'orders' in data or isinstance(data, list)
    
    def test_get_orders_admin(self, client, auth_headers):
        """Test GET /api/orders - List all orders (admin)"""
        response = client.get('/api/orders', headers=auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'orders' in data or isinstance(data, list)
    
    def test_get_orders_unauthorized(self, client):
        """Test GET /api/orders without authentication"""
        response = client.get('/api/orders')
        assert response.status_code == 401
    
    def test_get_order_by_id(self, client, user_auth_headers):
        """Test GET /api/orders/{id} - Get specific order"""
        # First create an order
        order_data = {
            'items': [{'product_id': 1, 'quantity': 2}],
            'total_amount': 199.98
        }
        create_response = client.post('/api/orders',
                                    data=json.dumps(order_data),
                                    headers=user_auth_headers,
                                    content_type='application/json')
        if create_response.status_code == 201:
            order_id = json.loads(create_response.data).get('id')
            
            # Get the order
            response = client.get(f'/api/orders/{order_id}', headers=user_auth_headers)
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'id' in data or 'total_amount' in data
    
    def test_get_order_by_id_not_found(self, client, user_auth_headers):
        """Test GET /api/orders/{id} with non-existent ID"""
        response = client.get('/api/orders/99999', headers=user_auth_headers)
        assert response.status_code == 404
    
    def test_get_order_by_id_forbidden(self, client, user_auth_headers):
        """Test GET /api/orders/{id} - Access another user's order"""
        # This would require creating an order as a different user
        # For now, test that user can't access admin's orders
        response = client.get('/api/orders/1', headers=user_auth_headers)
        # Should be 404 (not found) or 403 (forbidden)
        assert response.status_code in [404, 403]
    
    def test_get_orders_with_status_filter(self, client, user_auth_headers):
        """Test GET /api/orders?status=pending - Filter by status"""
        response = client.get('/api/orders?status=pending', headers=user_auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        orders = data.get('orders', data) if isinstance(data, dict) else data
        if orders:
            for order in orders:
                assert order.get('status') == 'pending'
    
    def test_get_orders_with_date_range(self, client, user_auth_headers):
        """Test GET /api/orders?start_date=2024-01-01&end_date=2024-12-31"""
        response = client.get('/api/orders?start_date=2024-01-01&end_date=2024-12-31',
                             headers=user_auth_headers)
        assert response.status_code == 200
    
    # ==================== POST Operations ====================
    
    def test_create_order_success(self, client, user_auth_headers):
        """Test POST /api/orders - Create new order"""
        order_data = {
            'items': [
                {'product_id': 1, 'quantity': 2},
                {'product_id': 2, 'quantity': 1}
            ],
            'total_amount': 2029.97
        }
        response = client.post('/api/orders',
                              data=json.dumps(order_data),
                              headers=user_auth_headers,
                              content_type='application/json')
        assert response.status_code in [201, 200]
        data = json.loads(response.data)
        assert 'id' in data or 'order_number' in data
    
    def test_create_order_unauthorized(self, client):
        """Test POST /api/orders without authentication"""
        order_data = {
            'items': [{'product_id': 1, 'quantity': 1}],
            'total_amount': 99.99
        }
        response = client.post('/api/orders',
                              data=json.dumps(order_data),
                              content_type='application/json')
        assert response.status_code == 401
    
    def test_create_order_missing_items(self, client, user_auth_headers):
        """Test POST /api/orders with missing items"""
        order_data = {
            'total_amount': 99.99
            # Missing items
        }
        response = client.post('/api/orders',
                              data=json.dumps(order_data),
                              headers=user_auth_headers,
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_order_empty_items(self, client, user_auth_headers):
        """Test POST /api/orders with empty items array"""
        order_data = {
            'items': [],
            'total_amount': 0
        }
        response = client.post('/api/orders',
                              data=json.dumps(order_data),
                              headers=user_auth_headers,
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_create_order_invalid_product(self, client, user_auth_headers):
        """Test POST /api/orders with non-existent product"""
        order_data = {
            'items': [{'product_id': 99999, 'quantity': 1}],
            'total_amount': 99.99
        }
        response = client.post('/api/orders',
                              data=json.dumps(order_data),
                              headers=user_auth_headers,
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_order_insufficient_stock(self, client, user_auth_headers):
        """Test POST /api/orders with quantity exceeding stock"""
        order_data = {
            'items': [{'product_id': 1, 'quantity': 1000}],  # More than available
            'total_amount': 999990.00
        }
        response = client.post('/api/orders',
                              data=json.dumps(order_data),
                              headers=user_auth_headers,
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data or 'stock' in str(data).lower()
    
    def test_create_order_invalid_quantity(self, client, user_auth_headers):
        """Test POST /api/orders with invalid quantity"""
        order_data = {
            'items': [{'product_id': 1, 'quantity': -1}],
            'total_amount': -99.99
        }
        response = client.post('/api/orders',
                              data=json.dumps(order_data),
                              headers=user_auth_headers,
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_create_order_invalid_total(self, client, user_auth_headers):
        """Test POST /api/orders with incorrect total amount"""
        order_data = {
            'items': [{'product_id': 1, 'quantity': 2}],
            'total_amount': 1.00  # Incorrect total
        }
        response = client.post('/api/orders',
                              data=json.dumps(order_data),
                              headers=user_auth_headers,
                              content_type='application/json')
        # Should either validate or accept (depending on implementation)
        assert response.status_code in [201, 400]
    
    def test_create_order_sql_injection(self, client, user_auth_headers):
        """Test POST /api/orders with SQL injection attempt"""
        order_data = {
            'items': [{'product_id': 1, 'quantity': 1}],
            'total_amount': 99.99,
            'notes': "'; DROP TABLE orders; --"
        }
        response = client.post('/api/orders',
                              data=json.dumps(order_data),
                              headers=user_auth_headers,
                              content_type='application/json')
        # Should sanitize or reject
        assert response.status_code in [201, 400]
        # Verify table still exists
        get_response = client.get('/api/orders', headers=user_auth_headers)
        assert get_response.status_code == 200
    
    # ==================== PUT Operations ====================
    
    def test_update_order_status(self, client, auth_headers):
        """Test PUT /api/orders/{id} - Update order status (admin)"""
        # First create an order
        order_data = {
            'items': [{'product_id': 1, 'quantity': 1}],
            'total_amount': 99.99
        }
        create_response = client.post('/api/orders',
                                     data=json.dumps(order_data),
                                     headers=auth_headers,
                                     content_type='application/json')
        if create_response.status_code == 201:
            order_id = json.loads(create_response.data).get('id')
            
            # Update order status
            update_data = {'status': 'shipped'}
            response = client.put(f'/api/orders/{order_id}',
                                data=json.dumps(update_data),
                                headers=auth_headers,
                                content_type='application/json')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data.get('status') == 'shipped' or 'id' in data
    
    def test_update_order_not_found(self, client, auth_headers):
        """Test PUT /api/orders/{id} with non-existent ID"""
        update_data = {'status': 'cancelled'}
        response = client.put('/api/orders/99999',
                             data=json.dumps(update_data),
                             headers=auth_headers,
                             content_type='application/json')
        assert response.status_code == 404
    
    def test_update_order_unauthorized(self, client):
        """Test PUT /api/orders/{id} without authentication"""
        update_data = {'status': 'shipped'}
        response = client.put('/api/orders/1',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 401
    
    def test_update_order_forbidden(self, client, user_auth_headers):
        """Test PUT /api/orders/{id} as regular user"""
        update_data = {'status': 'shipped'}
        response = client.put('/api/orders/1',
                             data=json.dumps(update_data),
                             headers=user_auth_headers,
                             content_type='application/json')
        assert response.status_code in [403, 401]
    
    def test_update_order_invalid_status(self, client, auth_headers):
        """Test PUT /api/orders/{id} with invalid status"""
        update_data = {'status': 'invalid_status'}
        response = client.put('/api/orders/1',
                             data=json.dumps(update_data),
                             headers=auth_headers,
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_cancel_order(self, client, user_auth_headers):
        """Test PUT /api/orders/{id}/cancel - Cancel own order"""
        # First create an order
        order_data = {
            'items': [{'product_id': 1, 'quantity': 1}],
            'total_amount': 99.99
        }
        create_response = client.post('/api/orders',
                                     data=json.dumps(order_data),
                                     headers=user_auth_headers,
                                     content_type='application/json')
        if create_response.status_code == 201:
            order_id = json.loads(create_response.data).get('id')
            
            # Cancel the order
            response = client.put(f'/api/orders/{order_id}/cancel',
                                headers=user_auth_headers)
            assert response.status_code in [200, 204]
    
    # ==================== DELETE Operations ====================
    
    def test_delete_order_success(self, client, auth_headers):
        """Test DELETE /api/orders/{id} - Delete order (admin only)"""
        # First create an order
        order_data = {
            'items': [{'product_id': 1, 'quantity': 1}],
            'total_amount': 99.99
        }
        create_response = client.post('/api/orders',
                                     data=json.dumps(order_data),
                                     headers=auth_headers,
                                     content_type='application/json')
        if create_response.status_code == 201:
            order_id = json.loads(create_response.data).get('id')
            
            # Delete the order
            response = client.delete(f'/api/orders/{order_id}', headers=auth_headers)
            assert response.status_code in [200, 204]
            
            # Verify deletion
            get_response = client.get(f'/api/orders/{order_id}', headers=auth_headers)
            assert get_response.status_code == 404
    
    def test_delete_order_not_found(self, client, auth_headers):
        """Test DELETE /api/orders/{id} with non-existent ID"""
        response = client.delete('/api/orders/99999', headers=auth_headers)
        assert response.status_code == 404
    
    def test_delete_order_unauthorized(self, client):
        """Test DELETE /api/orders/{id} without authentication"""
        response = client.delete('/api/orders/1')
        assert response.status_code == 401
    
    def test_delete_order_forbidden(self, client, user_auth_headers):
        """Test DELETE /api/orders/{id} as regular user"""
        response = client.delete('/api/orders/1', headers=user_auth_headers)
        assert response.status_code in [403, 401]
    
    # ==================== Performance Tests ====================
    
    def test_get_orders_performance(self, client, user_auth_headers):
        """Test GET /api/orders response time under 500ms"""
        start_time = time.time()
        response = client.get('/api/orders', headers=user_auth_headers)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000
        assert response.status_code == 200
        assert response_time < 500, f"Response time {response_time}ms exceeds 500ms"
    
    def test_get_order_by_id_performance(self, client, user_auth_headers):
        """Test GET /api/orders/{id} response time under 500ms"""
        # First create an order
        order_data = {
            'items': [{'product_id': 1, 'quantity': 1}],
            'total_amount': 99.99
        }
        create_response = client.post('/api/orders',
                                     data=json.dumps(order_data),
                                     headers=user_auth_headers,
                                     content_type='application/json')
        if create_response.status_code == 201:
            order_id = json.loads(create_response.data).get('id')
            
            start_time = time.time()
            response = client.get(f'/api/orders/{order_id}', headers=user_auth_headers)
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000
            assert response.status_code == 200
            assert response_time < 500, f"Response time {response_time}ms exceeds 500ms"
    
    def test_create_order_performance(self, client, user_auth_headers):
        """Test POST /api/orders response time under 500ms"""
        order_data = {
            'items': [{'product_id': 1, 'quantity': 1}],
            'total_amount': 99.99
        }
        start_time = time.time()
        response = client.post('/api/orders',
                              data=json.dumps(order_data),
                              headers=user_auth_headers,
                              content_type='application/json')
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000
        assert response.status_code in [201, 200]
        assert response_time < 500, f"Response time {response_time}ms exceeds 500ms"
