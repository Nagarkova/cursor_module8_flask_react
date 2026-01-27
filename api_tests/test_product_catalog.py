"""
Comprehensive API tests for Product Catalog endpoints
Tests GET, POST, PUT, DELETE operations with authentication, authorization, and validation
"""
import pytest
import json
import time

class TestProductCatalog:
    """Product Catalog API Tests"""
    
    # ==================== GET Operations ====================
    
    def test_get_products_list(self, client):
        """Test GET /api/products - List all products (public endpoint)"""
        response = client.get('/api/products')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'products' in data or isinstance(data, list)
        assert len(data.get('products', data)) > 0
    
    def test_get_products_with_pagination(self, client):
        """Test GET /api/products?page=1&limit=10 - Paginated products"""
        response = client.get('/api/products?page=1&limit=10')
        assert response.status_code == 200
        data = json.loads(response.data)
        # Should have pagination metadata or limited results
        assert 'products' in data or isinstance(data, list)
        if isinstance(data, dict):
            products = data.get('products', [])
            assert len(products) <= 10
    
    def test_get_products_with_filter(self, client):
        """Test GET /api/products?category=Electronics - Filtered products"""
        response = client.get('/api/products?category=Electronics')
        assert response.status_code == 200
        data = json.loads(response.data)
        products = data.get('products', data) if isinstance(data, dict) else data
        if products:
            # Verify all products match filter
            for product in products:
                assert product.get('category') == 'Electronics'
    
    def test_get_products_with_search(self, client):
        """Test GET /api/products?search=laptop - Search products"""
        response = client.get('/api/products?search=laptop')
        assert response.status_code == 200
        data = json.loads(response.data)
        products = data.get('products', data) if isinstance(data, dict) else data
        # Results should contain search term (case-insensitive)
        if products:
            found = any('laptop' in str(product).lower() for product in products)
            assert found or len(products) == 0
    
    def test_get_product_by_id(self, client):
        """Test GET /api/products/{id} - Get specific product"""
        response = client.get('/api/products/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'id' in data or 'name' in data
        assert data.get('id') == 1 or 'name' in data
    
    def test_get_product_by_id_not_found(self, client):
        """Test GET /api/products/{id} with non-existent ID"""
        response = client.get('/api/products/99999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data or 'message' in data
    
    def test_get_product_by_id_invalid_format(self, client):
        """Test GET /api/products/{id} with invalid ID format"""
        response = client.get('/api/products/invalid')
        assert response.status_code in [400, 404]
    
    def test_get_products_sorted(self, client):
        """Test GET /api/products?sort=price&order=asc - Sorted products"""
        response = client.get('/api/products?sort=price&order=asc')
        assert response.status_code == 200
        data = json.loads(response.data)
        products = data.get('products', data) if isinstance(data, dict) else data
        if len(products) > 1:
            prices = [p.get('price', 0) for p in products if 'price' in p]
            assert prices == sorted(prices)
    
    # ==================== POST Operations ====================
    
    def test_create_product_success(self, client, auth_headers):
        """Test POST /api/products - Create new product (admin only)"""
        product_data = {
            'name': 'New Product',
            'description': 'Test product description',
            'price': 99.99,
            'stock': 100,
            'category': 'Test'
        }
        response = client.post('/api/products',
                              data=json.dumps(product_data),
                              headers=auth_headers,
                              content_type='application/json')
        assert response.status_code in [201, 200]
        data = json.loads(response.data)
        assert 'id' in data or 'name' in data
        assert data.get('name') == 'New Product' or 'product' in str(data).lower()
    
    def test_create_product_unauthorized(self, client):
        """Test POST /api/products without authentication"""
        product_data = {
            'name': 'Test Product',
            'price': 99.99
        }
        response = client.post('/api/products',
                             data=json.dumps(product_data),
                             content_type='application/json')
        assert response.status_code == 401
    
    def test_create_product_forbidden(self, client, user_auth_headers):
        """Test POST /api/products as regular user"""
        product_data = {
            'name': 'Test Product',
            'price': 99.99
        }
        response = client.post('/api/products',
                             data=json.dumps(product_data),
                             headers=user_auth_headers,
                             content_type='application/json')
        assert response.status_code in [403, 401]
    
    def test_create_product_missing_fields(self, client, auth_headers):
        """Test POST /api/products with missing required fields"""
        product_data = {
            'name': 'Incomplete Product'
            # Missing price
        }
        response = client.post('/api/products',
                              data=json.dumps(product_data),
                              headers=auth_headers,
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_product_invalid_price(self, client, auth_headers):
        """Test POST /api/products with invalid price"""
        product_data = {
            'name': 'Test Product',
            'price': -10.00  # Negative price
        }
        response = client.post('/api/products',
                              data=json.dumps(product_data),
                              headers=auth_headers,
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data or 'price' in str(data).lower()
    
    def test_create_product_invalid_stock(self, client, auth_headers):
        """Test POST /api/products with invalid stock"""
        product_data = {
            'name': 'Test Product',
            'price': 99.99,
            'stock': -5  # Negative stock
        }
        response = client.post('/api/products',
                              data=json.dumps(product_data),
                              headers=auth_headers,
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_create_product_sql_injection(self, client, auth_headers):
        """Test POST /api/products with SQL injection attempt"""
        product_data = {
            'name': "Product'; DROP TABLE products; --",
            'price': 99.99,
            'description': 'Test'
        }
        response = client.post('/api/products',
                              data=json.dumps(product_data),
                              headers=auth_headers,
                              content_type='application/json')
        # Should sanitize or reject
        assert response.status_code in [201, 400]
        # Verify table still exists
        get_response = client.get('/api/products')
        assert get_response.status_code == 200
    
    def test_create_product_xss_attempt(self, client, auth_headers):
        """Test POST /api/products with XSS attempt"""
        product_data = {
            'name': '<script>alert("XSS")</script>',
            'price': 99.99,
            'description': '<img src=x onerror=alert("XSS")>'
        }
        response = client.post('/api/products',
                              data=json.dumps(product_data),
                              headers=auth_headers,
                              content_type='application/json')
        # Should sanitize input
        assert response.status_code in [201, 400]
        if response.status_code == 201:
            data = json.loads(response.data)
            assert '<script>' not in str(data)
    
    # ==================== PUT Operations ====================
    
    def test_update_product_success(self, client, auth_headers):
        """Test PUT /api/products/{id} - Update product"""
        update_data = {
            'name': 'Updated Product',
            'price': 149.99
        }
        response = client.put('/api/products/1',
                             data=json.dumps(update_data),
                             headers=auth_headers,
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data.get('name') == 'Updated Product' or 'id' in data
    
    def test_update_product_not_found(self, client, auth_headers):
        """Test PUT /api/products/{id} with non-existent ID"""
        update_data = {'name': 'Updated'}
        response = client.put('/api/products/99999',
                             data=json.dumps(update_data),
                             headers=auth_headers,
                             content_type='application/json')
        assert response.status_code == 404
    
    def test_update_product_unauthorized(self, client):
        """Test PUT /api/products/{id} without authentication"""
        update_data = {'name': 'Updated'}
        response = client.put('/api/products/1',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 401
    
    def test_update_product_forbidden(self, client, user_auth_headers):
        """Test PUT /api/products/{id} as regular user"""
        update_data = {'name': 'Hacked'}
        response = client.put('/api/products/1',
                             data=json.dumps(update_data),
                             headers=user_auth_headers,
                             content_type='application/json')
        assert response.status_code in [403, 401]
    
    def test_update_product_invalid_data(self, client, auth_headers):
        """Test PUT /api/products/{id} with invalid data"""
        update_data = {'price': -50.00}
        response = client.put('/api/products/1',
                             data=json.dumps(update_data),
                             headers=auth_headers,
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_update_product_partial(self, client, auth_headers):
        """Test PUT /api/products/{id} with partial update"""
        update_data = {'stock': 200}
        response = client.put('/api/products/1',
                             data=json.dumps(update_data),
                             headers=auth_headers,
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data.get('stock') == 200 or 'id' in data
    
    # ==================== DELETE Operations ====================
    
    def test_delete_product_success(self, client, auth_headers):
        """Test DELETE /api/products/{id} - Delete product (admin only)"""
        # First create a product to delete
        product_data = {
            'name': 'To Delete',
            'price': 50.00,
            'stock': 10
        }
        create_response = client.post('/api/products',
                                      data=json.dumps(product_data),
                                      headers=auth_headers,
                                      content_type='application/json')
        if create_response.status_code == 201:
            product_id = json.loads(create_response.data).get('id')
            
            # Delete the product
            response = client.delete(f'/api/products/{product_id}', headers=auth_headers)
            assert response.status_code in [200, 204]
            
            # Verify deletion
            get_response = client.get(f'/api/products/{product_id}')
            assert get_response.status_code == 404
    
    def test_delete_product_not_found(self, client, auth_headers):
        """Test DELETE /api/products/{id} with non-existent ID"""
        response = client.delete('/api/products/99999', headers=auth_headers)
        assert response.status_code == 404
    
    def test_delete_product_unauthorized(self, client):
        """Test DELETE /api/products/{id} without authentication"""
        response = client.delete('/api/products/1')
        assert response.status_code == 401
    
    def test_delete_product_forbidden(self, client, user_auth_headers):
        """Test DELETE /api/products/{id} as regular user"""
        response = client.delete('/api/products/1', headers=user_auth_headers)
        assert response.status_code in [403, 401]
    
    # ==================== Performance Tests ====================
    
    def test_get_products_performance(self, client):
        """Test GET /api/products response time under 500ms"""
        start_time = time.time()
        response = client.get('/api/products')
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000
        assert response.status_code == 200
        assert response_time < 500, f"Response time {response_time}ms exceeds 500ms"
    
    def test_get_product_by_id_performance(self, client):
        """Test GET /api/products/{id} response time under 500ms"""
        start_time = time.time()
        response = client.get('/api/products/1')
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000
        assert response.status_code == 200
        assert response_time < 500, f"Response time {response_time}ms exceeds 500ms"
    
    def test_create_product_performance(self, client, auth_headers):
        """Test POST /api/products response time under 500ms"""
        product_data = {
            'name': f'PerfProduct{int(time.time())}',
            'price': 99.99,
            'stock': 10
        }
        start_time = time.time()
        response = client.post('/api/products',
                              data=json.dumps(product_data),
                              headers=auth_headers,
                              content_type='application/json')
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000
        assert response.status_code in [201, 200]
        assert response_time < 500, f"Response time {response_time}ms exceeds 500ms"
    
    def test_get_products_with_filters_performance(self, client):
        """Test GET /api/products with filters response time under 500ms"""
        start_time = time.time()
        response = client.get('/api/products?category=Electronics&page=1&limit=10')
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000
        assert response.status_code == 200
        assert response_time < 500, f"Response time {response_time}ms exceeds 500ms"
