"""
Test Data Generation Strategy
Generates realistic test data for comprehensive testing
"""
import random
import string
from datetime import datetime, timedelta, timezone
from faker import Faker

fake = Faker()

class TestDataGenerator:
    """Generate test data for e-commerce checkout tests"""
    
    @staticmethod
    def generate_session_id():
        """Generate unique session ID"""
        return f'session_{datetime.now().timestamp()}_{random.randint(1000, 9999)}'
    
    @staticmethod
    def generate_email():
        """Generate valid email address"""
        return fake.email()
    
    @staticmethod
    def generate_invalid_email():
        """Generate invalid email addresses"""
        invalid_emails = [
            'notanemail',
            '@example.com',
            'test@',
            'test..test@example.com',
            'test@example',
            'test @example.com',
            'test@.com',
            'test@example..com',
        ]
        return random.choice(invalid_emails)
    
    @staticmethod
    def generate_card_number(valid=True, card_type='visa'):
        """Generate credit card numbers"""
        if not valid:
            invalid_cards = [
                '1234',  # Too short
                '12345678901234567890',  # Too long
                'abcd1234567890',  # Contains letters
                '0000000000000000',  # All zeros
                '1111111111111111',  # All ones
            ]
            return random.choice(invalid_cards)
        
        # Valid test card numbers (Luhn algorithm compliant)
        card_numbers = {
            'visa': '4111111111111111',
            'mastercard': '5555555555554444',
            'amex': '378282246310005',
            'discover': '6011111111111117',
        }
        return card_numbers.get(card_type, card_numbers['visa'])
    
    @staticmethod
    def generate_cvv(valid=True):
        """Generate CVV codes"""
        if not valid:
            invalid_cvvs = ['12', '12345', 'abc', '12a', '00', '000']
            return random.choice(invalid_cvvs)
        return str(random.randint(100, 9999)).zfill(3 if random.choice([True, False]) else 4)
    
    @staticmethod
    def generate_expiry_date(valid=True):
        """Generate expiry dates"""
        if not valid:
            invalid_dates = ['12/20', '01/19', '00/25', '13/25', '12/99']
            return random.choice(invalid_dates)
        
        # Future date
        future_date = datetime.now() + timedelta(days=random.randint(30, 365*3))
        return future_date.strftime('%m/%y')
    
    @staticmethod
    def generate_shipping_address():
        """Generate shipping address"""
        return fake.address().replace('\n', ', ')
    
    @staticmethod
    def generate_discount_code():
        """Generate discount code"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    @staticmethod
    def generate_sql_injection_payload():
        """Generate SQL injection test payloads"""
        payloads = [
            "'; DROP TABLE orders; --",
            "'; DROP TABLE cart_items; --",
            "'; DROP TABLE discount_codes; --",
            "' OR '1'='1",
            "' UNION SELECT * FROM orders --",
            "'; INSERT INTO orders VALUES (1, 'hack'); --",
            "1' OR '1'='1",
            "admin'--",
            "' OR 1=1--",
        ]
        return random.choice(payloads)
    
    @staticmethod
    def generate_xss_payload():
        """Generate XSS test payloads"""
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src='javascript:alert(\"XSS\")'></iframe>",
            "<body onload=alert('XSS')>",
        ]
        return random.choice(payloads)
    
    @staticmethod
    def generate_product_data():
        """Generate product test data"""
        return {
            'name': fake.word().capitalize() + ' ' + fake.word().capitalize(),
            'price': round(random.uniform(10.0, 1000.0), 2),
            'description': fake.text(max_nb_chars=100),
            'stock': random.randint(0, 100),
        }
    
    @staticmethod
    def generate_discount_code_data(active=True, expired=False):
        """Generate discount code test data"""
        expiry_date = None
        if expired:
            expiry_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 30))
        elif active:
            expiry_date = datetime.now(timezone.utc) + timedelta(days=random.randint(1, 365))
        
        return {
            'code': ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
            'discount_percent': round(random.uniform(5.0, 50.0), 2),
            'is_active': active and not expired,
            'expiry_date': expiry_date,
        }
    
    @staticmethod
    def generate_checkout_data(session_id, valid=True, include_discount=False):
        """Generate complete checkout data"""
        data = {
            'session_id': session_id,
            'email': TestDataGenerator.generate_email() if valid else TestDataGenerator.generate_invalid_email(),
            'payment_method': 'card',
            'card_number': TestDataGenerator.generate_card_number(valid=valid),
            'cvv': TestDataGenerator.generate_cvv(valid=valid),
            'expiry_date': TestDataGenerator.generate_expiry_date(valid=valid),
            'shipping_address': TestDataGenerator.generate_shipping_address(),
        }
        
        if include_discount:
            data['discount_code'] = TestDataGenerator.generate_discount_code()
        
        return data
