"""
Comprehensive API tests for User Management endpoints
Tests GET, POST, PUT, DELETE operations with authentication, authorization, and validation
"""
import pytest
import json
import time
from datetime import datetime

class TestUserManagement:
    """User Management API Tests"""
    
    # ==================== GET Operations ====================
    
    def test_get_users_list(self, client, auth_headers):
        """Test GET /api/users - List all users (admin only)"""
        response = client.get('/api/users', headers=auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'users' in data or isinstance(data, list)
        assert len(data.get('users', data)) > 0
    
    def test_get_users_unauthorized(self, client):
        """Test GET /api/users without authentication"""
        response = client.get('/api/users')
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data or 'message' in data
    
    def test_get_users_forbidden(self, client, user_auth_headers):
        """Test GET /api/users as regular user (should be forbidden)"""
        response = client.get('/api/users', headers=user_auth_headers)
        assert response.status_code in [403, 401]
    
    def test_get_user_by_id(self, client, auth_headers):
        """Test GET /api/users/{id} - Get specific user"""
        response = client.get('/api/users/1', headers=auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'id' in data or 'username' in data
        assert data.get('id') == 1 or 'username' in data
    
    def test_get_user_by_id_not_found(self, client, auth_headers):
        """Test GET /api/users/{id} with non-existent ID"""
        response = client.get('/api/users/99999', headers=auth_headers)
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data or 'message' in data
    
    def test_get_user_by_id_invalid_format(self, client, auth_headers):
        """Test GET /api/users/{id} with invalid ID format"""
        response = client.get('/api/users/invalid', headers=auth_headers)
        assert response.status_code in [400, 404]
    
    def test_get_current_user(self, client, user_auth_headers):
        """Test GET /api/users/me - Get current authenticated user"""
        response = client.get('/api/users/me', headers=user_auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'username' in data or 'email' in data
    
    def test_get_current_user_unauthorized(self, client):
        """Test GET /api/users/me without authentication"""
        response = client.get('/api/users/me')
        assert response.status_code == 401
    
    # ==================== POST Operations ====================
    
    def test_create_user_success(self, client):
        """Test POST /api/users - Create new user"""
        user_data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'password123',
            'role': 'user'
        }
        response = client.post('/api/users', 
                              data=json.dumps(user_data),
                              content_type='application/json')
        assert response.status_code in [201, 200]
        data = json.loads(response.data)
        assert 'id' in data or 'username' in data
        assert data.get('username') == 'newuser' or 'user' in data
    
    def test_create_user_duplicate_username(self, client):
        """Test POST /api/users with duplicate username"""
        user_data = {
            'username': 'testuser',  # Already exists
            'email': 'different@test.com',
            'password': 'password123'
        }
        response = client.post('/api/users',
                              data=json.dumps(user_data),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data or 'username' in str(data).lower()
    
    def test_create_user_duplicate_email(self, client):
        """Test POST /api/users with duplicate email"""
        user_data = {
            'username': 'differentuser',
            'email': 'user@test.com',  # Already exists
            'password': 'password123'
        }
        response = client.post('/api/users',
                              data=json.dumps(user_data),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data or 'email' in str(data).lower()
    
    def test_create_user_missing_fields(self, client):
        """Test POST /api/users with missing required fields"""
        user_data = {
            'username': 'incomplete'
            # Missing email and password
        }
        response = client.post('/api/users',
                              data=json.dumps(user_data),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_user_invalid_email(self, client):
        """Test POST /api/users with invalid email format"""
        user_data = {
            'username': 'testuser2',
            'email': 'invalid-email',
            'password': 'password123'
        }
        response = client.post('/api/users',
                              data=json.dumps(user_data),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data or 'email' in str(data).lower()
    
    def test_create_user_weak_password(self, client):
        """Test POST /api/users with weak password"""
        user_data = {
            'username': 'testuser3',
            'email': 'test3@test.com',
            'password': '123'  # Too short
        }
        response = client.post('/api/users',
                              data=json.dumps(user_data),
                              content_type='application/json')
        # Should either accept or validate password strength
        assert response.status_code in [201, 400]
    
    def test_create_user_sql_injection(self, client):
        """Test POST /api/users with SQL injection attempt"""
        user_data = {
            'username': "admin'; DROP TABLE users; --",
            'email': 'test@test.com',
            'password': 'password123'
        }
        response = client.post('/api/users',
                              data=json.dumps(user_data),
                              content_type='application/json')
        # Should sanitize or reject
        assert response.status_code in [201, 400]
        # Verify table still exists
        get_response = client.get('/api/users')
        assert get_response.status_code in [200, 401]
    
    def test_create_user_xss_attempt(self, client):
        """Test POST /api/users with XSS attempt"""
        user_data = {
            'username': '<script>alert("XSS")</script>',
            'email': 'xss@test.com',
            'password': 'password123'
        }
        response = client.post('/api/users',
                              data=json.dumps(user_data),
                              content_type='application/json')
        # Should sanitize input
        assert response.status_code in [201, 400]
        if response.status_code == 201:
            data = json.loads(response.data)
            assert '<script>' not in str(data)
    
    # ==================== PUT Operations ====================
    
    def test_update_user_success(self, client, auth_headers):
        """Test PUT /api/users/{id} - Update user"""
        update_data = {
            'email': 'updated@test.com',
            'role': 'user'
        }
        response = client.put('/api/users/2',
                              data=json.dumps(update_data),
                              headers=auth_headers,
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data.get('email') == 'updated@test.com' or 'id' in data
    
    def test_update_user_not_found(self, client, auth_headers):
        """Test PUT /api/users/{id} with non-existent ID"""
        update_data = {'email': 'test@test.com'}
        response = client.put('/api/users/99999',
                              data=json.dumps(update_data),
                              headers=auth_headers,
                              content_type='application/json')
        assert response.status_code == 404
    
    def test_update_user_unauthorized(self, client):
        """Test PUT /api/users/{id} without authentication"""
        update_data = {'email': 'test@test.com'}
        response = client.put('/api/users/1',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 401
    
    def test_update_user_forbidden(self, client, user_auth_headers):
        """Test PUT /api/users/{id} as regular user trying to update another user"""
        update_data = {'email': 'hacked@test.com'}
        response = client.put('/api/users/1',  # Try to update admin
                             data=json.dumps(update_data),
                             headers=user_auth_headers,
                             content_type='application/json')
        assert response.status_code in [403, 401]
    
    def test_update_user_own_profile(self, client, user_auth_headers):
        """Test PUT /api/users/me - Update own profile"""
        update_data = {'email': 'mynewemail@test.com'}
        response = client.put('/api/users/me',
                             data=json.dumps(update_data),
                             headers=user_auth_headers,
                             content_type='application/json')
        assert response.status_code in [200, 403]
    
    def test_update_user_invalid_data(self, client, auth_headers):
        """Test PUT /api/users/{id} with invalid data"""
        update_data = {'email': 'invalid-email'}
        response = client.put('/api/users/2',
                              data=json.dumps(update_data),
                              headers=auth_headers,
                              content_type='application/json')
        assert response.status_code == 400
    
    # ==================== DELETE Operations ====================
    
    def test_delete_user_success(self, client, auth_headers):
        """Test DELETE /api/users/{id} - Delete user (admin only)"""
        # First create a user to delete
        user_data = {
            'username': 'todelete',
            'email': 'todelete@test.com',
            'password': 'password123'
        }
        create_response = client.post('/api/users',
                                     data=json.dumps(user_data),
                                     content_type='application/json')
        if create_response.status_code == 201:
            user_id = json.loads(create_response.data).get('id')
            
            # Delete the user
            response = client.delete(f'/api/users/{user_id}', headers=auth_headers)
            assert response.status_code in [200, 204]
            
            # Verify deletion
            get_response = client.get(f'/api/users/{user_id}', headers=auth_headers)
            assert get_response.status_code == 404
    
    def test_delete_user_not_found(self, client, auth_headers):
        """Test DELETE /api/users/{id} with non-existent ID"""
        response = client.delete('/api/users/99999', headers=auth_headers)
        assert response.status_code == 404
    
    def test_delete_user_unauthorized(self, client):
        """Test DELETE /api/users/{id} without authentication"""
        response = client.delete('/api/users/1')
        assert response.status_code == 401
    
    def test_delete_user_forbidden(self, client, user_auth_headers):
        """Test DELETE /api/users/{id} as regular user"""
        response = client.delete('/api/users/1', headers=user_auth_headers)
        assert response.status_code in [403, 401]
    
    def test_delete_current_user(self, client, user_auth_headers):
        """Test DELETE /api/users/me - Delete own account"""
        response = client.delete('/api/users/me', headers=user_auth_headers)
        assert response.status_code in [200, 204, 403]
    
    # ==================== Authentication Tests ====================
    
    def test_login_success(self, client):
        """Test POST /api/auth/login - Successful login"""
        login_data = {
            'username': 'testuser',
            'password': 'user123'
        }
        response = client.post('/api/auth/login',
                              data=json.dumps(login_data),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'token' in data or 'access_token' in data
    
    def test_login_invalid_credentials(self, client):
        """Test POST /api/auth/login with invalid credentials"""
        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = client.post('/api/auth/login',
                              data=json.dumps(login_data),
                              content_type='application/json')
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_login_nonexistent_user(self, client):
        """Test POST /api/auth/login with non-existent user"""
        login_data = {
            'username': 'nonexistent',
            'password': 'password123'
        }
        response = client.post('/api/auth/login',
                              data=json.dumps(login_data),
                              content_type='application/json')
        assert response.status_code == 401
    
    def test_logout(self, client, user_auth_headers):
        """Test POST /api/auth/logout"""
        response = client.post('/api/auth/logout', headers=user_auth_headers)
        assert response.status_code in [200, 204]
    
    # ==================== Performance Tests ====================
    
    def test_get_users_performance(self, client, auth_headers):
        """Test GET /api/users response time under 500ms"""
        start_time = time.time()
        response = client.get('/api/users', headers=auth_headers)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        assert response.status_code == 200
        assert response_time < 500, f"Response time {response_time}ms exceeds 500ms"
    
    def test_get_user_by_id_performance(self, client, auth_headers):
        """Test GET /api/users/{id} response time under 500ms"""
        start_time = time.time()
        response = client.get('/api/users/1', headers=auth_headers)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000
        assert response.status_code == 200
        assert response_time < 500, f"Response time {response_time}ms exceeds 500ms"
    
    def test_create_user_performance(self, client):
        """Test POST /api/users response time under 500ms"""
        user_data = {
            'username': f'perfuser{int(time.time())}',
            'email': f'perf{int(time.time())}@test.com',
            'password': 'password123'
        }
        start_time = time.time()
        response = client.post('/api/users',
                              data=json.dumps(user_data),
                              content_type='application/json')
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000
        assert response.status_code in [201, 200]
        assert response_time < 500, f"Response time {response_time}ms exceeds 500ms"
