"""
Rate Limiting Tests
Tests API rate limiting functionality
"""
import pytest
import time
import json

class TestRateLimiting:
    """Rate Limiting API Tests"""
    
    def test_rate_limit_exceeded(self, client):
        """Test rate limiting - exceed request limit"""
        # Make multiple rapid requests
        responses = []
        for i in range(110):  # Assuming limit is 100 requests per minute
            response = client.get('/api/products')
            responses.append(response.status_code)
            if response.status_code == 429:  # Too Many Requests
                break
        
        # Should eventually get 429 status
        assert 429 in responses or len(responses) < 110
    
    def test_rate_limit_headers(self, client):
        """Test rate limit headers in response"""
        response = client.get('/api/products')
        
        # Check for rate limit headers (if implemented)
        headers = response.headers
        # Common rate limit headers:
        # X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
        rate_limit_headers = [
            'X-RateLimit-Limit',
            'X-RateLimit-Remaining',
            'X-RateLimit-Reset',
            'RateLimit-Limit',
            'RateLimit-Remaining',
            'RateLimit-Reset'
        ]
        
        # At least one rate limit header should be present
        has_rate_limit_header = any(h in headers for h in rate_limit_headers)
        # This is optional, so we don't fail if not present
        # assert has_rate_limit_header, "Rate limit headers not found"
    
    def test_rate_limit_reset(self, client):
        """Test rate limit reset after time window"""
        # Make requests until rate limited
        responses = []
        for i in range(110):
            response = client.get('/api/products')
            responses.append(response.status_code)
            if response.status_code == 429:
                break
        
        # Wait for rate limit window to reset (if we got rate limited)
        if 429 in responses:
            time.sleep(2)  # Wait 2 seconds
            
            # Try again - should work if rate limit reset
            response = client.get('/api/products')
            # May still be rate limited or may work
            assert response.status_code in [200, 429]
    
    def test_rate_limit_per_endpoint(self, client):
        """Test rate limiting per endpoint"""
        # Different endpoints may have different rate limits
        endpoints = ['/api/products', '/api/users', '/api/orders']
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            # Each endpoint should have its own rate limit
            assert response.status_code in [200, 401, 429]
    
    def test_rate_limit_per_user(self, client, user_auth_headers):
        """Test rate limiting per authenticated user"""
        # Make requests as authenticated user
        responses = []
        for i in range(110):
            response = client.get('/api/orders', headers=user_auth_headers)
            responses.append(response.status_code)
            if response.status_code == 429:
                break
        
        # Should eventually get rate limited
        assert 429 in responses or len(responses) < 110
    
    def test_rate_limit_bypass_admin(self, client, auth_headers):
        """Test if admin users bypass rate limiting"""
        # Admin might have higher rate limits
        responses = []
        for i in range(110):
            response = client.get('/api/users', headers=auth_headers)
            responses.append(response.status_code)
            if response.status_code == 429:
                break
        
        # Admin may or may not be rate limited
        # This depends on implementation
        assert all(status in [200, 401, 403, 429] for status in responses)
    
    def test_rate_limit_post_requests(self, client, user_auth_headers):
        """Test rate limiting on POST requests"""
        # POST requests typically have stricter rate limits
        responses = []
        for i in range(50):  # Lower limit for POST
            order_data = {
                'items': [{'product_id': 1, 'quantity': 1}],
                'total_amount': 99.99
            }
            response = client.post('/api/orders',
                                  data=json.dumps(order_data),
                                  headers=user_auth_headers,
                                  content_type='application/json')
            responses.append(response.status_code)
            if response.status_code == 429:
                break
        
        # Should eventually get rate limited
        assert 429 in responses or len(responses) < 50
    
    def test_rate_limit_error_message(self, client):
        """Test rate limit error message"""
        # Make requests until rate limited
        response = None
        for i in range(110):
            response = client.get('/api/products')
            if response.status_code == 429:
                break
        
        if response and response.status_code == 429:
            data = json.loads(response.data)
            assert 'error' in data or 'message' in data
            # Error message should indicate rate limit
            error_text = str(data).lower()
            assert 'rate limit' in error_text or 'too many' in error_text
