# E-Commerce Checkout Full Stack Application

A comprehensive full-stack e-commerce checkout application with React frontend and Flask backend, including extensive test coverage.

## Features

- **Product Catalog**: Browse and view available products
- **Shopping Cart**: Add, update, and remove items from cart
- **Discount Codes**: Apply discount codes to orders
- **Checkout Process**: Secure payment processing with validation
- **Order Confirmation**: Order tracking and email notifications
- **Comprehensive Testing**: Extensive test suite covering positive, negative, edge cases, and security scenarios

## Tech Stack

### Backend
- Flask (Python web framework)
- SQLAlchemy (ORM)
- Flask-Mail (Email notifications)
- Flask-CORS (Cross-origin resource sharing)
- pytest (Testing framework)

### Frontend
- React 18
- Axios (HTTP client)
- React Router (Navigation)

## Project Structure

```
.
├── backend/
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   └── test_checkout.py      # Comprehensive test suite
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── App.js            # Main app component
│   │   └── index.js          # Entry point
│   └── package.json          # Node dependencies
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file (optional, for email configuration):
```env
SECRET_KEY=your-secret-key-here
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

5. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## Running Tests

### Backend Tests (Pytest)

From the backend directory:

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest test_checkout.py test_checkout_expanded.py -v

# Run with coverage
pytest test_checkout.py test_checkout_expanded.py --cov=app --cov-report=html

# Run specific test class
pytest test_checkout.py::TestPositiveScenarios -v
pytest test_checkout_expanded.py::TestSecurityAndPCICompliance -v

# Run specific test
pytest test_checkout.py::TestPositiveScenarios::test_add_item_to_cart_success -v
```

### Frontend Tests (Jest)

From the frontend directory:

```bash
# Install dependencies (if not already done)
npm install

# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage

# Run specific test file
npm test -- App.test.js
```

## Test Coverage

The test suite (`test_checkout.py`) includes comprehensive test cases:

### Positive Scenarios
- ✅ Adding items to cart
- ✅ Retrieving cart contents
- ✅ Applying valid discount codes
- ✅ Successful checkout with valid payment
- ✅ Checkout with discount code
- ✅ Updating cart quantities
- ✅ Removing items from cart
- ✅ Order retrieval

### Negative Scenarios
- ❌ Missing required fields
- ❌ Invalid product IDs
- ❌ Invalid quantities
- ❌ Invalid discount codes
- ❌ Inactive/expired discount codes
- ❌ Invalid email addresses
- ❌ Invalid payment card numbers
- ❌ Invalid CVV codes
- ❌ Payment declined scenarios

### Edge Cases
- 🔍 Empty cart checkout
- 🔍 Applying discount to empty cart
- 🔍 Adding items exceeding stock
- 🔍 Adding out-of-stock products
- 🔍 Multiple additions of same product
- 🔍 Updating cart exceeding stock
- 🔍 Missing required fields

### Security Scenarios
- 🔒 SQL injection prevention in session_id
- 🔒 SQL injection prevention in discount codes
- 🔒 XSS prevention in shipping address
- 🔒 SQL injection prevention in email
- 🔒 Payment data validation
- 🔒 CVV validation
- 🔒 Email validation
- 🔒 Cross-session cart access prevention
- 🔒 Special character handling

### Integration Tests
- 🔗 Complete checkout flow
- 🔗 Stock reduction after checkout

## API Endpoints

### Products
- `GET /api/products` - Get all products

### Cart
- `GET /api/cart?session_id=<id>` - Get cart items
- `POST /api/cart/add` - Add item to cart
- `POST /api/cart/remove` - Remove item from cart
- `POST /api/cart/update` - Update cart item quantity

### Discount
- `POST /api/discount/apply` - Apply discount code

### Checkout
- `POST /api/checkout` - Process checkout and payment

### Orders
- `GET /api/orders/<order_number>` - Get order details

## Sample Data

The application includes sample data:
- Products: Laptop, Mouse, Keyboard, Monitor
- Discount Codes: SAVE10 (10% off), WELCOME20 (20% off)

## Security Features

- Input sanitization to prevent SQL injection
- Email validation
- Payment card number validation
- CVV validation
- Session-based cart isolation
- XSS prevention through input sanitization

## Notes

- The application uses SQLite for development (can be easily switched to PostgreSQL/MySQL)
- Email functionality requires proper SMTP configuration
- Payment processing is simulated (integrate with real payment gateway for production)
- Session management uses localStorage in frontend (consider server-side sessions for production)

## License

MIT License
