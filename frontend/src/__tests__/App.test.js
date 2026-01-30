/**
 * Jest test suite for React frontend components
 * Tests user interactions, API calls, and component rendering
 */
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import axios from 'axios';
import App from '../App';
import ProductList from '../components/ProductList';
import Cart from '../components/Cart';
import Checkout from '../components/Checkout';
import OrderConfirmation from '../components/OrderConfirmation';

// Mock axios
jest.mock('axios');

describe('App Component', () => {
  beforeEach(() => {
    localStorage.clear();
    jest.clearAllMocks();
    
    // Mock initial cart fetch
    axios.get.mockResolvedValue({ data: { items: [], total: 0, item_count: 0 } });
  });

  test('renders app header with navigation', async () => {
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('E-Commerce Checkout')).toBeInTheDocument();
    });
    
    const productButtons = screen.getAllByText(/Products/i);
    const cartButtons = screen.getAllByText(/Cart/i);
    expect(productButtons.length).toBeGreaterThan(0);
    expect(cartButtons.length).toBeGreaterThan(0);
  });

  test('switches between Products and Cart views', async () => {
    // Mock products and cart data
    const mockProducts = [
      { id: 1, name: 'Laptop', price: 999.99, description: 'High-performance laptop', stock: 10 },
    ];
    
    axios.get.mockImplementation((url) => {
      if (url.includes('/api/products')) {
        return Promise.resolve({ data: mockProducts });
      }
      return Promise.resolve({ data: { items: [], total: 0, item_count: 0 } });
    });
    
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('E-Commerce Checkout')).toBeInTheDocument();
      expect(screen.getByText('Laptop')).toBeInTheDocument();
    });
    
    const cartButtons = screen.getAllByText(/Cart/i);
    fireEvent.click(cartButtons[0]);
    
    await waitFor(() => {
      const cartHeadings = screen.getAllByText(/Your Cart/i);
      expect(cartHeadings.length).toBeGreaterThan(0);
    });
  });
});

describe('ProductList Component', () => {
  const mockProducts = [
    { id: 1, name: 'Laptop', price: 999.99, description: 'High-performance laptop', stock: 10 },
    { id: 2, name: 'Mouse', price: 29.99, description: 'Wireless mouse', stock: 50 },
  ];

  test('renders product list', async () => {
    axios.get.mockResolvedValue({ data: mockProducts });
    render(<ProductList addToCart={jest.fn()} />);
    
    await waitFor(() => {
      expect(screen.getByText('Laptop')).toBeInTheDocument();
      expect(screen.getByText('Mouse')).toBeInTheDocument();
    });
  });

  test('calls addToCart when Add to Cart button is clicked', async () => {
    const mockAddToCart = jest.fn();
    axios.get.mockResolvedValue({ data: mockProducts });
    render(<ProductList addToCart={mockAddToCart} />);
    
    await waitFor(() => {
      const addButtons = screen.getAllByText('Add to Cart');
      fireEvent.click(addButtons[0]);
      expect(mockAddToCart).toHaveBeenCalledWith(1, 1);
    });
  });

  test('disables Add to Cart for out of stock products', async () => {
    const outOfStockProducts = [
      { id: 1, name: 'Product', price: 100, description: 'Test', stock: 0 },
    ];
    axios.get.mockResolvedValue({ data: outOfStockProducts });
    render(<ProductList addToCart={jest.fn()} />);
    
    await waitFor(() => {
      expect(screen.getByText('Out of Stock')).toBeInTheDocument();
    });
  });
});

describe('Cart Component', () => {
  const mockCart = {
    items: [
      {
        id: 1,
        product_id: 1,
        product_name: 'Laptop',
        price: 999.99,
        quantity: 1,
        subtotal: 999.99,
      },
      {
        id: 2,
        product_id: 2,
        product_name: 'Mouse',
        price: 29.99,
        quantity: 2,
        subtotal: 59.98,
      },
    ],
    total: 1059.97,
    item_count: 2,
  };

  test('renders cart items', () => {
    render(
      <Cart
        cart={mockCart}
        removeFromCart={jest.fn()}
        updateCartQuantity={jest.fn()}
        onCheckout={jest.fn()}
      />
    );
    
    expect(screen.getByText('Laptop')).toBeInTheDocument();
    expect(screen.getByText('Mouse')).toBeInTheDocument();
    expect(screen.getByText('$1059.97')).toBeInTheDocument();
  });

  test('displays empty cart message when cart is empty', () => {
    const emptyCart = { items: [], total: 0, item_count: 0 };
    render(
      <Cart
        cart={emptyCart}
        removeFromCart={jest.fn()}
        updateCartQuantity={jest.fn()}
        onCheckout={jest.fn()}
      />
    );
    
    expect(screen.getByText(/Your cart is empty/i)).toBeInTheDocument();
  });

  test('calls removeFromCart when Remove button is clicked', () => {
    const mockRemoveFromCart = jest.fn();
    render(
      <Cart
        cart={mockCart}
        removeFromCart={mockRemoveFromCart}
        updateCartQuantity={jest.fn()}
        onCheckout={jest.fn()}
      />
    );
    
    const removeButtons = screen.getAllByText('Remove');
    fireEvent.click(removeButtons[0]);
    expect(mockRemoveFromCart).toHaveBeenCalledWith(1);
  });

  test('calls updateCartQuantity when quantity is changed', () => {
    const mockUpdateCartQuantity = jest.fn();
    render(
      <Cart
        cart={mockCart}
        removeFromCart={jest.fn()}
        updateCartQuantity={mockUpdateCartQuantity}
        onCheckout={jest.fn()}
      />
    );
    
    const quantityInputs = screen.getAllByDisplayValue('1');
    fireEvent.change(quantityInputs[0], { target: { value: '3' } });
    expect(mockUpdateCartQuantity).toHaveBeenCalledWith(1, 3);
  });

  test('calls onCheckout when Proceed to Checkout is clicked', () => {
    const mockOnCheckout = jest.fn();
    render(
      <Cart
        cart={mockCart}
        removeFromCart={jest.fn()}
        updateCartQuantity={jest.fn()}
        onCheckout={mockOnCheckout}
      />
    );
    
    const checkoutButton = screen.getByText('Proceed to Checkout');
    fireEvent.click(checkoutButton);
    expect(mockOnCheckout).toHaveBeenCalled();
  });
});

describe('Checkout Component', () => {
  const mockCart = {
    items: [{ id: 1, product_name: 'Laptop', quantity: 1, subtotal: 999.99 }],
    total: 999.99,
    item_count: 1,
  };

  test('renders checkout form', () => {
    render(
      <Checkout
        sessionId="test_session"
        cart={mockCart}
        onSuccess={jest.fn()}
        onBack={jest.fn()}
      />
    );
    
    expect(screen.getByLabelText(/Email Address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Shipping Address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Payment Method/i)).toBeInTheDocument();
  });

  test('validates email format', async () => {
    const mockOnSuccess = jest.fn();
    axios.post.mockResolvedValue({ data: { order_number: 'ORD123', status: 'confirmed' } });
    
    render(
      <Checkout
        sessionId="test_session"
        cart={mockCart}
        onSuccess={mockOnSuccess}
        onBack={jest.fn()}
      />
    );
    
    const emailInput = screen.getByLabelText(/Email Address/i);
    fireEvent.change(emailInput, { target: { value: 'invalid-email' } });
    
    const submitButton = screen.getByText('Place Order');
    fireEvent.click(submitButton);
    
    // HTML5 validation should prevent submission
    await waitFor(() => {
      expect(emailInput).toBeInvalid();
    });
  });

  test('applies discount code', async () => {
    axios.post.mockResolvedValueOnce({
      data: {
        discount_code: 'SAVE10',
        discount_percent: 10,
        original_total: 999.99,
        discount_amount: 99.99,
        final_total: 900.00,
      },
    });
    
    render(
      <Checkout
        sessionId="test_session"
        cart={mockCart}
        onSuccess={jest.fn()}
        onBack={jest.fn()}
      />
    );
    
    const discountInput = screen.getByPlaceholderText(/Enter discount code/i);
    const applyButton = screen.getByText('Apply');
    
    fireEvent.change(discountInput, { target: { value: 'SAVE10' } });
    fireEvent.click(applyButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Discount applied successfully/i)).toBeInTheDocument();
    });
  });

  test('handles discount code error', async () => {
    axios.post.mockRejectedValueOnce({
      response: { data: { error: 'Invalid discount code' } },
    });
    
    render(
      <Checkout
        sessionId="test_session"
        cart={mockCart}
        onSuccess={jest.fn()}
        onBack={jest.fn()}
      />
    );
    
    const discountInput = screen.getByPlaceholderText(/Enter discount code/i);
    const applyButton = screen.getByText('Apply');
    
    fireEvent.change(discountInput, { target: { value: 'INVALID' } });
    fireEvent.click(applyButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Invalid discount code/i)).toBeInTheDocument();
    });
  });

  test('submits checkout form successfully', async () => {
    const mockOnSuccess = jest.fn();
    axios.post.mockResolvedValue({
      data: { order_number: 'ORD123', status: 'confirmed', total_amount: 999.99 },
    });
    
    render(
      <Checkout
        sessionId="test_session"
        cart={mockCart}
        onSuccess={mockOnSuccess}
        onBack={jest.fn()}
      />
    );
    
    // Fill form
    fireEvent.change(screen.getByLabelText(/Email Address/i), {
      target: { value: 'test@example.com' },
    });
    fireEvent.change(screen.getByLabelText(/Shipping Address/i), {
      target: { value: '123 Test St' },
    });
    fireEvent.change(screen.getByLabelText(/Card Number/i), {
      target: { value: '4111111111111111' },
    });
    fireEvent.change(screen.getByLabelText(/CVV/i), {
      target: { value: '123' },
    });
    fireEvent.change(screen.getByLabelText(/Expiry Date/i), {
      target: { value: '12/25' },
    });
    
    const submitButton = screen.getByText('Place Order');
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(mockOnSuccess).toHaveBeenCalled();
    });
  });

  test('handles checkout error', async () => {
    axios.post.mockRejectedValueOnce({
      response: { data: { error: 'Payment declined' } },
    });
    
    render(
      <Checkout
        sessionId="test_session"
        cart={mockCart}
        onSuccess={jest.fn()}
        onBack={jest.fn()}
      />
    );
    
    // Fill form
    fireEvent.change(screen.getByLabelText(/Email Address/i), {
      target: { value: 'test@example.com' },
    });
    fireEvent.change(screen.getByLabelText(/Shipping Address/i), {
      target: { value: '123 Test St' },
    });
    fireEvent.change(screen.getByLabelText(/Card Number/i), {
      target: { value: '4111111111111111' },
    });
    fireEvent.change(screen.getByLabelText(/CVV/i), {
      target: { value: '123' },
    });
    fireEvent.change(screen.getByLabelText(/Expiry Date/i), {
      target: { value: '12/25' },
    });
    
    const submitButton = screen.getByText('Place Order');
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Payment declined/i)).toBeInTheDocument();
    });
  });
});

describe('OrderConfirmation Component', () => {
  const mockOrder = {
    order_number: 'ORD-20240127123456-abc12345',
    status: 'confirmed',
    total_amount: 999.99,
  };

  test('renders order confirmation', () => {
    render(<OrderConfirmation order={mockOrder} />);
    
    expect(screen.getByText(/Order Confirmed/i)).toBeInTheDocument();
    expect(screen.getByText(new RegExp(mockOrder.order_number))).toBeInTheDocument();
    expect(screen.getByText('$999.99')).toBeInTheDocument();
  });

  test('displays order status', () => {
    render(<OrderConfirmation order={mockOrder} />);
    
    expect(screen.getByText(/Status/i)).toBeInTheDocument();
    expect(screen.getByText('confirmed')).toBeInTheDocument();
  });
});
