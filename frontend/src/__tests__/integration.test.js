/**
 * Integration tests for complete checkout flow
 * Tests end-to-end user journeys
 */
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import axios from 'axios';
import App from '../App';

jest.mock('axios');

describe('Complete Checkout Flow Integration Tests', () => {
  beforeEach(() => {
    localStorage.clear();
    jest.clearAllMocks();
  });

  test('complete checkout flow: browse -> add to cart -> checkout -> confirm', async () => {
    // Mock API responses
    const mockProducts = [
      { id: 1, name: 'Laptop', price: 999.99, description: 'High-performance laptop', stock: 10 },
    ];
    
    const mockCart = {
      items: [
        { id: 1, product_id: 1, product_name: 'Laptop', price: 999.99, quantity: 1, subtotal: 999.99 },
      ],
      total: 999.99,
      item_count: 1,
    };
    
    const mockOrder = {
      order_number: 'ORD-123',
      status: 'confirmed',
      total_amount: 999.99,
    };

    axios.get
      .mockResolvedValueOnce({ data: mockProducts }) // Products
      .mockResolvedValueOnce({ data: mockCart }); // Cart

    axios.post
      .mockResolvedValueOnce({ data: { message: 'Item added to cart successfully' } }) // Add to cart
      .mockResolvedValueOnce({ data: mockOrder }); // Checkout

    render(<App />);

    // Step 1: View products
    await waitFor(() => {
      expect(screen.getByText('Laptop')).toBeInTheDocument();
    });

    // Step 2: Add to cart
    const addToCartButton = screen.getByText('Add to Cart');
    fireEvent.click(addToCartButton);

    await waitFor(() => {
      expect(axios.post).toHaveBeenCalledWith('/api/cart/add', expect.any(Object));
    });

    // Step 3: View cart
    const cartButton = screen.getByText(/Cart/i);
    fireEvent.click(cartButton);

    await waitFor(() => {
      expect(screen.getByText('Laptop')).toBeInTheDocument();
    });

    // Step 4: Proceed to checkout
    const checkoutButton = screen.getByText('Proceed to Checkout');
    fireEvent.click(checkoutButton);

    await waitFor(() => {
      expect(screen.getByLabelText(/Email Address/i)).toBeInTheDocument();
    });

    // Step 5: Fill checkout form
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

    // Step 6: Submit order
    const placeOrderButton = screen.getByText('Place Order');
    fireEvent.click(placeOrderButton);

    // Step 7: Verify order confirmation
    await waitFor(() => {
      expect(screen.getByText(/Order Confirmed/i)).toBeInTheDocument();
      expect(screen.getByText('ORD-123')).toBeInTheDocument();
    });
  });

  test('checkout flow with discount code', async () => {
    const mockProducts = [
      { id: 1, name: 'Laptop', price: 1000.0, description: 'Laptop', stock: 10 },
    ];
    
    const mockCart = {
      items: [{ id: 1, product_id: 1, product_name: 'Laptop', price: 1000.0, quantity: 1, subtotal: 1000.0 }],
      total: 1000.0,
      item_count: 1,
    };

    axios.get
      .mockResolvedValueOnce({ data: mockProducts })
      .mockResolvedValueOnce({ data: mockCart });

    axios.post
      .mockResolvedValueOnce({ data: { message: 'Item added' } })
      .mockResolvedValueOnce({
        data: {
          discount_code: 'SAVE10',
          discount_percent: 10,
          original_total: 1000.0,
          discount_amount: 100.0,
          final_total: 900.0,
        },
      })
      .mockResolvedValueOnce({
        data: { order_number: 'ORD-123', status: 'confirmed', total_amount: 900.0 },
      });

    render(<App />);

    // Add to cart and go to checkout
    await waitFor(() => screen.getByText('Add to Cart'));
    fireEvent.click(screen.getByText('Add to Cart'));
    
    await waitFor(() => screen.getByText(/Cart/i));
    fireEvent.click(screen.getByText(/Cart/i));
    
    await waitFor(() => screen.getByText('Proceed to Checkout'));
    fireEvent.click(screen.getByText('Proceed to Checkout'));

    // Apply discount
    await waitFor(() => screen.getByPlaceholderText(/Enter discount code/i));
    const discountInput = screen.getByPlaceholderText(/Enter discount code/i);
    fireEvent.change(discountInput, { target: { value: 'SAVE10' } });
    fireEvent.click(screen.getByText('Apply'));

    await waitFor(() => {
      expect(screen.getByText(/Discount applied successfully/i)).toBeInTheDocument();
      expect(screen.getByText('$900.00')).toBeInTheDocument();
    });
  });

  test('error handling: product out of stock', async () => {
    const mockProducts = [
      { id: 1, name: 'Laptop', price: 999.99, description: 'Laptop', stock: 0 },
    ];

    axios.get.mockResolvedValue({ data: mockProducts });

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Out of Stock')).toBeInTheDocument();
      const addButton = screen.getByText('Out of Stock');
      expect(addButton).toBeDisabled();
    });
  });

  test('error handling: invalid discount code', async () => {
    const mockCart = {
      items: [{ id: 1, product_name: 'Laptop', quantity: 1, subtotal: 1000.0 }],
      total: 1000.0,
      item_count: 1,
    };

    axios.get.mockResolvedValue({ data: mockCart });
    axios.post
      .mockRejectedValueOnce({
        response: { data: { error: 'Invalid discount code' } },
      });

    render(<App />);

    // Navigate to checkout
    const cartButton = screen.getByText(/Cart/i);
    fireEvent.click(cartButton);

    await waitFor(() => screen.getByText('Proceed to Checkout'));
    fireEvent.click(screen.getByText('Proceed to Checkout'));

    // Try invalid discount
    await waitFor(() => screen.getByPlaceholderText(/Enter discount code/i));
    const discountInput = screen.getByPlaceholderText(/Enter discount code/i);
    fireEvent.change(discountInput, { target: { value: 'INVALID' } });
    fireEvent.click(screen.getByText('Apply'));

    await waitFor(() => {
      expect(screen.getByText(/Invalid discount code/i)).toBeInTheDocument();
    });
  });
});
