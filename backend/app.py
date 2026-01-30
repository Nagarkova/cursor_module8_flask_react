from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
import re
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Email configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')

CORS(app)
db = SQLAlchemy(app)
mail = Mail(app)

# Database Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, default=0)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    product = db.relationship('Product', backref='cart_items')

class DiscountCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    discount_percent = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    expiry_date = db.Column(db.DateTime)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    session_id = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), default='pending')
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    payment_method = db.Column(db.String(50))
    shipping_address = db.Column(db.Text)

# Validation helpers
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_card_number(card_number):
    # Remove spaces and dashes
    card_number = re.sub(r'[\s-]', '', card_number)
    # Check if it's 13-19 digits
    return re.match(r'^\d{13,19}$', card_number) is not None

def validate_cvv(cvv):
    return re.match(r'^\d{3,4}$', cvv) is not None

def sanitize_input(input_str):
    """Prevent SQL injection by escaping special characters"""
    if not input_str:
        return ""
    # Remove SQL injection patterns
    dangerous_patterns = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)",
        r"(--|;|\*|'|%)",  # Removed underscore from dangerous patterns
    ]
    sanitized = input_str
    for pattern in dangerous_patterns:
        sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
    return sanitized.strip()

# API Routes
@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'description': p.description,
        'stock': p.stock
    } for p in products])

@app.route('/api/cart', methods=['GET'])
def get_cart():
    """Get cart items for a session"""
    session_id = request.args.get('session_id')
    if not session_id:
        return jsonify({'error': 'session_id required'}), 400
    
    items = CartItem.query.filter_by(session_id=session_id).all()
    cart_total = 0
    cart_items = []
    
    for item in items:
        cart_items.append({
            'id': item.id,
            'product_id': item.product_id,
            'product_name': item.product.name,
            'price': item.product.price,
            'quantity': item.quantity,
            'subtotal': item.product.price * item.quantity
        })
        cart_total += item.product.price * item.quantity
    
    return jsonify({
        'items': cart_items,
        'total': cart_total,
        'item_count': len(cart_items)
    })

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    data = request.json
    
    # Validate input
    session_id = sanitize_input(data.get('session_id', ''))
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not session_id or not product_id:
        return jsonify({'error': 'session_id and product_id required'}), 400
    
    if not isinstance(product_id, int) or product_id <= 0:
        return jsonify({'error': 'Invalid product_id'}), 400
    
    if not isinstance(quantity, int) or quantity <= 0:
        return jsonify({'error': 'Invalid quantity'}), 400
    
    # Check if product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Check stock
    if product.stock < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    # Check if item already in cart
    existing_item = CartItem.query.filter_by(
        session_id=session_id,
        product_id=product_id
    ).first()
    
    if existing_item:
        new_quantity = existing_item.quantity + quantity
        if product.stock < new_quantity:
            return jsonify({'error': 'Insufficient stock'}), 400
        existing_item.quantity = new_quantity
    else:
        new_item = CartItem(
            session_id=session_id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(new_item)
    
    db.session.commit()
    return jsonify({'message': 'Item added to cart successfully'}), 201

@app.route('/api/cart/remove', methods=['POST'])
def remove_from_cart():
    """Remove item from cart"""
    data = request.json
    session_id = sanitize_input(data.get('session_id', ''))
    item_id = data.get('item_id')
    
    if not session_id or not item_id:
        return jsonify({'error': 'session_id and item_id required'}), 400
    
    item = CartItem.query.filter_by(id=item_id, session_id=session_id).first()
    if not item:
        return jsonify({'error': 'Item not found in cart'}), 404
    
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item removed from cart'}), 200

@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    """Update cart item quantity"""
    data = request.json
    session_id = sanitize_input(data.get('session_id', ''))
    item_id = data.get('item_id')
    quantity = data.get('quantity')
    
    if not session_id or not item_id or quantity is None:
        return jsonify({'error': 'session_id, item_id, and quantity required'}), 400
    
    if not isinstance(quantity, int) or quantity <= 0:
        return jsonify({'error': 'Invalid quantity'}), 400
    
    item = CartItem.query.filter_by(id=item_id, session_id=session_id).first()
    if not item:
        return jsonify({'error': 'Item not found in cart'}), 404
    
    if item.product.stock < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    item.quantity = quantity
    db.session.commit()
    return jsonify({'message': 'Cart updated successfully'}), 200

@app.route('/api/discount/apply', methods=['POST'])
def apply_discount():
    """Apply discount code"""
    data = request.json
    code = sanitize_input(data.get('code', ''))
    session_id = sanitize_input(data.get('session_id', ''))
    
    if not code or not session_id:
        return jsonify({'error': 'code and session_id required'}), 400
    
    discount = DiscountCode.query.filter_by(code=code.upper()).first()
    
    if not discount:
        return jsonify({'error': 'Invalid discount code'}), 404
    
    if not discount.is_active:
        return jsonify({'error': 'Discount code is not active'}), 400
    
    if discount.expiry_date and discount.expiry_date < datetime.utcnow():
        return jsonify({'error': 'Discount code has expired'}), 400
    
    # Get cart total
    items = CartItem.query.filter_by(session_id=session_id).all()
    cart_total = sum(item.product.price * item.quantity for item in items)
    
    if cart_total == 0:
        return jsonify({'error': 'Cart is empty'}), 400
    
    discount_amount = cart_total * (discount.discount_percent / 100)
    final_total = cart_total - discount_amount
    
    return jsonify({
        'discount_code': discount.code,
        'discount_percent': discount.discount_percent,
        'original_total': cart_total,
        'discount_amount': round(discount_amount, 2),
        'final_total': round(final_total, 2)
    }), 200

@app.route('/api/checkout', methods=['POST'])
def checkout():
    """Process checkout and payment"""
    data = request.json
    
    # Validate required fields
    session_id = sanitize_input(data.get('session_id', ''))
    email = data.get('email', '').strip()
    payment_method = sanitize_input(data.get('payment_method', ''))
    card_number = data.get('card_number', '')
    cvv = data.get('cvv', '')
    expiry_date = data.get('expiry_date', '')
    shipping_address = sanitize_input(data.get('shipping_address', ''))
    discount_code = sanitize_input(data.get('discount_code', ''))
    
    # Validation
    if not session_id:
        return jsonify({'error': 'session_id required'}), 400
    
    if not validate_email(email):
        return jsonify({'error': 'Invalid email address'}), 400
    
    # Get cart items
    cart_items = CartItem.query.filter_by(session_id=session_id).all()
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400
    
    # Calculate totals
    cart_total = sum(item.product.price * item.quantity for item in cart_items)
    discount_amount = 0.0
    
    # Apply discount if provided
    if discount_code:
        discount = DiscountCode.query.filter_by(code=discount_code.upper()).first()
        if discount and discount.is_active:
            if not discount.expiry_date or discount.expiry_date >= datetime.utcnow():
                discount_amount = cart_total * (discount.discount_percent / 100)
    
    final_total = cart_total - discount_amount
    
    # Validate payment
    if payment_method == 'card':
        if not card_number or not validate_card_number(card_number):
            return jsonify({'error': 'Invalid card number'}), 400
        
        if not cvv or not validate_cvv(cvv):
            return jsonify({'error': 'Invalid CVV'}), 400
        
        if not expiry_date:
            return jsonify({'error': 'Expiry date required'}), 400
        
        # Simulate payment processing
        # In production, integrate with payment gateway
        if card_number.endswith('0000'):
            return jsonify({'error': 'Payment declined'}), 400
    
    # Create order
    order_number = f"ORD-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{session_id[:8]}"
    order = Order(
        order_number=order_number,
        session_id=session_id,
        total_amount=final_total,
        discount_amount=discount_amount,
        status='confirmed',
        email=email,
        payment_method=payment_method,
        shipping_address=shipping_address
    )
    db.session.add(order)
    
    # Clear cart
    for item in cart_items:
        # Update product stock
        item.product.stock -= item.quantity
        db.session.delete(item)
    
    db.session.commit()
    
    # Send confirmation email
    try:
        send_order_confirmation_email(email, order_number, final_total)
    except Exception as e:
        # Log error but don't fail the order
        print(f"Email sending failed: {e}")
    
    return jsonify({
        'order_number': order_number,
        'status': 'confirmed',
        'total_amount': final_total,
        'message': 'Order placed successfully'
    }), 201

def send_order_confirmation_email(email, order_number, total_amount):
    """Send order confirmation email"""
    msg = Message(
        subject=f'Order Confirmation - {order_number}',
        recipients=[email],
        body=f'''
Thank you for your order!

Order Number: {order_number}
Total Amount: ${total_amount:.2f}

Your order has been confirmed and will be processed shortly.

Thank you for shopping with us!
        ''',
        sender=app.config['MAIL_USERNAME']
    )
    mail.send(msg)

@app.route('/api/orders/<order_number>', methods=['GET'])
def get_order(order_number):
    """Get order details"""
    order = Order.query.filter_by(order_number=order_number).first()
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    return jsonify({
        'order_number': order.order_number,
        'status': order.status,
        'total_amount': order.total_amount,
        'discount_amount': order.discount_amount,
        'email': order.email,
        'created_at': order.created_at.isoformat(),
        'payment_method': order.payment_method
    })

# Initialize database
def init_db():
    """Initialize database and seed sample data"""
    db.create_all()
    # Seed sample data
    if Product.query.count() == 0:
        products = [
            Product(name='Laptop', price=999.99, description='High-performance laptop', stock=10),
            Product(name='Mouse', price=29.99, description='Wireless mouse', stock=50),
            Product(name='Keyboard', price=79.99, description='Mechanical keyboard', stock=30),
            Product(name='Monitor', price=299.99, description='27-inch 4K monitor', stock=15),
        ]
        for product in products:
            db.session.add(product)
        
        discount_codes = [
            DiscountCode(code='SAVE10', discount_percent=10.0, is_active=True),
            DiscountCode(code='WELCOME20', discount_percent=20.0, is_active=True),
            DiscountCode(code='EXPIRED', discount_percent=15.0, is_active=False),
        ]
        for code in discount_codes:
            db.session.add(code)
        
        db.session.commit()

# Initialize database before first request
@app.before_request
def initialize_database():
    """Ensure database is initialized before processing any request"""
    if not hasattr(app, '_database_initialized'):
        with app.app_context():
            db.create_all()
            # Only seed if tables are empty
            if Product.query.count() == 0:
                products = [
                    Product(name='Laptop', price=999.99, description='High-performance laptop', stock=10),
                    Product(name='Mouse', price=29.99, description='Wireless mouse', stock=50),
                    Product(name='Keyboard', price=79.99, description='Mechanical keyboard', stock=30),
                    Product(name='Monitor', price=299.99, description='27-inch 4K monitor', stock=15),
                ]
                for product in products:
                    db.session.add(product)
                
                discount_codes = [
                    DiscountCode(code='SAVE10', discount_percent=10.0, is_active=True),
                    DiscountCode(code='WELCOME20', discount_percent=20.0, is_active=True),
                    DiscountCode(code='EXPIRED', discount_percent=15.0, is_active=False),
                ]
                for code in discount_codes:
                    db.session.add(code)
                
                db.session.commit()
            app._database_initialized = True

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)
