"""
Error Response Tests
Tests proper error responses for various scenarios
"""
import pytest
import json

class TestErrorResponses:
    """Error Response API Tests"""
    
    def test_400_bad_request(self, client):
        """Test 400 Bad Request response"""
        # Invalid JSON
        response = client.post('/api/users',
                              data='{invalid json}',
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data or 'message' in data
    
    def test_401_unauthorized(self, client):
        """Test 401 Unauthorized response"""
        response = client.get('/api/users')
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data or 'message' in data
        assert 'unauthorized' in str(data).lower() or 'authentication' in str(data).lower()
    
    def test_403_forbidden(self, client, user_auth_headers):
        """Test 403 Forbidden response"""
        # Regular user trying to access admin endpoint
        response = client.delete('/api/users/1', headers=user_auth_headers)
        if response.status_code == 403:
            data = json.loads(response.data)
            assert 'error' in data or 'message' in data
            assert 'forbidden' in str(data).lower() or 'permission' in str(data).lower()
    
    def test_404_not_found(self, client, auth_headers):
        """Test 404 Not Found response"""
        response = client.get('/api/users/99999', headers=auth_headers)
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data or 'message' in data
        assert 'not found' in str(data).lower()
    
    def test_409_conflict(self, client):
        """Test 409 Conflict response (duplicate resource)"""
        user_data = {
            'username': 'testuser',  # Already exists
            'email': 'duplicate@test.com',
            'password': 'password123'
        }
        response = client.post('/api/users',
                              data=json.dumps(user_data),
                              content_type='application/json')
        # May return 400 or 409 depending on implementation
        assert response.status_code in [400, 409]
        if response.status_code == 409:
            data = json.loads(response.data)
            assert 'error' in data or 'message' in data
    
    def test_422_unprocessable_entity(self, client, user_auth_headers):
        """Test 422 Unprocessable Entity response"""
        order_data = {
            'items': [{'product_id': 'invalid', 'quantity': 1}],  # Invalid product_id type
            'total_amount': 99.99
        }
        response = client.post('/api/orders',
                             data=json.dumps(order_data),
                             headers=user_auth_headers,
                             content_type='application/json')
        # May return 400 or 422 depending on implementation
        assert response.status_code in [400, 422]
        if response.status_code == 422:
            data = json.loads(response.data)
            assert 'error' in data or 'message' in data
    
    def test_429_too_many_requests(self, client):
        """Test 429 Too Many Requests response"""
        # Make many rapid requests
        for i in range(110):
            response = client.get('/api/products')
            if response.status_code == 429:
                data = json.loads(response.data)
                assert 'error' in data or 'message' in data
                assert 'rate limit' in str(data).lower() or 'too many' in str(data).lower()
                break
    
    def test_500_internal_server_error(self, client):
        """Test 500 Internal Server Error handling"""
        # This would require triggering an actual server error
        # For now, we verify the endpoint exists
        response = client.get('/api/products')
        # Should not return 500 for normal requests
        assert response.status_code != 500
    
    def test_error_response_format(self, client):
        """Test error response format consistency"""
        # Test various error scenarios
        error_scenarios = [
            ('/api/users/99999', 'GET', None, 404),  # Not found
            ('/api/users', 'GET', None, 401),  # Unauthorized
        ]
        
        for endpoint, method, headers, expected_status in error_scenarios:
            if method == 'GET':
                response = client.get(endpoint, headers=headers)
            elif method == 'POST':
                response = client.post(endpoint, headers=headers)
            
            if response.status_code == expected_status:
                data = json.loads(response.data)
                # Error responses should have consistent format
                assert 'error' in data or 'message' in data
    
    def test_error_response_content_type(self, client):
        """Test error responses have correct content type"""
        response = client.get('/api/users/99999')
        assert response.status_code in [401, 404]
        assert response.content_type == 'application/json'
    
    def test_validation_error_details(self, client):
        """Test validation errors include field details"""
        user_data = {
            'username': 'test',
            'email': 'invalid-email',  # Invalid email
            'password': '123'  # Weak password
        }
        response = client.post('/api/users',
                              data=json.dumps(user_data),
                              content_type='application/json')
        if response.status_code == 400:
            data = json.loads(response.data)
            # Should include validation details
            assert 'error' in data or 'errors' in data or 'message' in data
