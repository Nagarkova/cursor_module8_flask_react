"""
Pytest configuration and fixtures for API testing
"""
import pytest
import time
import jwt
from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

# Import your app (adjust import path as needed)
# For this example, we'll create a test app structure
@pytest.fixture(scope='session')
def app():
    """Create test Flask application"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['JWT_SECRET_KEY'] = 'test-jwt-secret'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    
    db = SQLAlchemy(app)
    
    # Define models for testing
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password_hash = db.Column(db.String(255), nullable=False)
        role = db.Column(db.String(20), default='user')
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        is_active = db.Column(db.Boolean, default=True)
    
    class Product(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        description = db.Column(db.Text)
        price = db.Column(db.Float, nullable=False)
        stock = db.Column(db.Integer, default=0)
        category = db.Column(db.String(50))
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    class Order(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        total_amount = db.Column(db.Float, nullable=False)
        status = db.Column(db.String(20), default='pending')
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        user = db.relationship('User', backref='orders')
    
    # Create tables
    with app.app_context():
        db.create_all()
        
        # Seed test data
        admin_user = User(
            username='admin',
            email='admin@test.com',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            is_active=True
        )
        regular_user = User(
            username='testuser',
            email='user@test.com',
            password_hash=generate_password_hash('user123'),
            role='user',
            is_active=True
        )
        db.session.add(admin_user)
        db.session.add(regular_user)
        
        # Add test products
        products = [
            Product(name='Laptop', description='High-performance laptop', price=999.99, stock=10, category='Electronics'),
            Product(name='Mouse', description='Wireless mouse', price=29.99, stock=50, category='Accessories'),
            Product(name='Keyboard', description='Mechanical keyboard', price=79.99, stock=30, category='Accessories'),
        ]
        for product in products:
            db.session.add(product)
        
        db.session.commit()
    
    yield app
    
    # Cleanup
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def db_session(app):
    """Create database session"""
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy(app)
    yield db
    db.session.rollback()

@pytest.fixture
def admin_token(app):
    """Generate admin JWT token"""
    payload = {
        'user_id': 1,
        'username': 'admin',
        'role': 'admin',
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token

@pytest.fixture
def user_token(app):
    """Generate regular user JWT token"""
    payload = {
        'user_id': 2,
        'username': 'testuser',
        'role': 'user',
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token

@pytest.fixture
def expired_token(app):
    """Generate expired JWT token"""
    payload = {
        'user_id': 1,
        'username': 'admin',
        'role': 'admin',
        'exp': datetime.utcnow() - timedelta(hours=1)
    }
    token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token

@pytest.fixture
def invalid_token():
    """Generate invalid JWT token"""
    return 'invalid.token.here'

@pytest.fixture
def auth_headers(admin_token):
    """Authorization headers with admin token"""
    return {'Authorization': f'Bearer {admin_token}'}

@pytest.fixture
def user_auth_headers(user_token):
    """Authorization headers with user token"""
    return {'Authorization': f'Bearer {user_token}'}

@pytest.fixture
def rate_limit_storage():
    """Storage for rate limiting tests"""
    return {}
